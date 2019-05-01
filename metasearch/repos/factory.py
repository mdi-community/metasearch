from ..fed import Federation

from . import openchemistry as oc
from . import hyperthought  as ht

def createDefaultFederation():
    """
    create a federation object from all repositories having an implementation
    here.
    """
    out = Federation()

    out.registerRepository("myHyperThought", ht.DEFAULT_BASE_URL, ht.htquery)
    out.registerRepository("openchemistry", oc.DEFAULT_BASE_URL,
                           oc.OpenChemistryQuery)

    return out
