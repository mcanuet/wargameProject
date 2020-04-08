#Version : 0.0.0

from random import *

"""
atq et l'attaquant exemple: a.compo["cavalier1"]
def et celui qui se fait attaquer exemple: b.compo["rejeton3"]

fonctionement:

Teste si atq réussi son attaque:
    si raté: fin
    si réussi: teste si deff esquive:
        si raté: teste si atq fait un critique:
            si raté: deff perd des pv normal
            si réussi: deff perd des pv avec atq.attaque*1.5
        si réussi: teste si deff contre-attaque:
            si raté: fin
            si réussi: attq pert des pv avec deff.attaque/2
"""

def pvRestant(atq,deff):

    if randint(0,100)<=atq.precision:
        if randint(0,100)>=deff.esquive:
            if randint(0,100)>=atq.critique:
                deff.pv = deff.pv-(atq.attaque*(1-deff.armure/100))
            deff.pv = deff.pv-(atq.attaque*1.5*(1-deff.armure/100))

        elif randint(0,100)<=deff.precision:
            atq.pv = atq.pv-((deff.attaque/2)*(1-atq.armure/100))
            return atq.pv

    return deff.pv
