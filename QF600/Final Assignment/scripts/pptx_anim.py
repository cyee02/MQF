"""Add Appear-on-click animations to named shapes (python-pptx has no API for it).

Usage from a builder:
    from pptx_anim import set_click_animations
    set_click_animations(slide, [["fig:fig02_ex3_bars"], ["txt:s3.takeaway", "num:ex3_eq_gap"]])

Each inner list is one click; shapes in the same list appear together.
Replaces any existing animation on the slide. The speaker notes must carry the
same number of [CLICK n] markers (checked by sync_check.py).
"""
from __future__ import annotations

from lxml import etree

P = "http://schemas.openxmlformats.org/presentationml/2006/main"


def _shape_id(slide, name: str) -> tuple[int, bool]:
    for sh in slide.shapes:
        if sh.name == name:
            return sh.shape_id, sh.has_text_frame
    raise KeyError(f"no shape named {name!r} on slide")


def set_click_animations(slide, clicks: list[list[str]]):
    sld = slide._element
    for old in sld.findall(f"{{{P}}}timing"):
        sld.remove(old)
    if not clicks:
        return

    ids = iter(range(3, 10_000))
    pars, builds = [], []
    for group in clicks:
        effects = []
        for k, name in enumerate(group):
            spid, has_text = _shape_id(slide, name)
            if has_text:
                builds.append(spid)
            node = "clickEffect" if k == 0 else "withEffect"
            a, b = next(ids), next(ids)
            effects.append(f"""
<p:par><p:cTn id="{a}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="{node}">
  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
  <p:childTnLst><p:set><p:cBhvr>
    <p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
    <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
    <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
  </p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set></p:childTnLst>
</p:cTn></p:par>""")
        outer, inner = next(ids), next(ids)
        pars.append(f"""
<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>
  <p:par><p:cTn id="{inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
    {''.join(effects)}
  </p:childTnLst></p:cTn></p:par>
</p:childTnLst></p:cTn></p:par>""")

    bld = "".join(f'<p:bldP spid="{i}" grpId="0"/>' for i in dict.fromkeys(builds))
    xml = f"""<p:timing xmlns:p="{P}"><p:tnLst><p:par>
<p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>
{''.join(pars)}
</p:childTnLst></p:cTn>
<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>
{'<p:bldLst>' + bld + '</p:bldLst>' if bld else ''}</p:timing>"""
    timing = etree.fromstring(xml)
    ext = sld.find(f"{{{P}}}extLst")
    if ext is not None:
        ext.addprevious(timing)
    else:
        sld.append(timing)


def click_count(slide) -> int:
    return slide._element.xml.count('nodeType="clickEffect"')
