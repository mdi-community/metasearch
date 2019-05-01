from ..fed import Federation

from . import openchemistry as oc
from . import hyperthought  as ht

def createDefaultFederation():
    """
    create a federation object from all repositories having an implementation
    here.
    """
    out = Federation()

    out.registerRepository("myHyperThought", ht.HTQuery, ht.DEFAULT_BASE_URL)
    out.registerRepository("openchemistry",
                           oc.OpenChemistryQuery, oc.DEFAULT_BASE_URL)

    return out
