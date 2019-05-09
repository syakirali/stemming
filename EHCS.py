class EHCS:
    def checkStem(self, stem):
        word_list = [line.rstrip('\n') for line in open('ehcs.txt')]
        if stem in word_list:
            return True
        return False

    def checkLengthStem(self, stem):
        if len(stem) > 3:
            return {'root': False, 'length': True, 'stem': stem}
        else:
            if (self.checkStem(stem)):
                return {'root': True, 'length': False, 'stem': stem}
            return {'root': False, 'length': False, 'stem': stem}

    def checkStemSame(self, stem):
        arr = stem.split("-")
        if len(arr) <= 1:
            return {'root': False,'stem': stem}
        elif arr[0] == arr[1]:
            if arr[0] is None or arr[0] == '':
                if self.checkStem(arr[1]):
                    return {'root': True, 'stem': arr[1]}
                return {'root': False, 'stem': arr[1]}
            elif arr[1] is None or arr[1] == '':
                if self.checkStem(arr[0]):
                    return {'root': True, 'stem': arr[0]}
                return {'root': False, 'stem': arr[0]}
        return {'root': False, 'stem': arr[1]}

    def checkRulePrecedence(self, stem):
        if stem[0:2] == "be" and stem[-3:] == "lah":
            return self.deleteDerivationBeC1C2(stem)
        elif stem[0:2] == "be" and stem[-2:] == "an":
            return self.deleteDerivationBeC1C2(stem)
        elif stem[0:2] == "di" and stem[-1:] == "i":
            return self.deleteDerivationDi(stem)
        elif stem[0:2] == "pe" and stem[-1:] == "i":
            return self.deleteDerivationPe(stem)
        elif stem[0:2] == "te" and stem[-1:] == "i":
            return self.deleteDerivationTeC1C2(stem)
        elif stem[0:2] == "me" and stem[-1:] == "i":
            return self.deleteDerivationMeV(stem)
        else:
            return {'root': False, 'stem': stem}

    def checkParticle(self, stem):
        if stem[-3:] == "lah":
            return self.deleteParticle(stem)
        elif stem[-3:] == "tah":
            return self.deleteParticle(stem)
        elif stem[-3:] == "kah":
            return self.deleteParticle(stem)
        elif stem[-3:] == "pun":
            return self.deleteParticle(stem)
        else:
            return {'root': False, 'stem': stem}

    def checkProssessivePronoun(self, stem):
        if stem[-2:] == "ku":
            return self.deleteProccessivePronoun(stem, 2)
        elif stem[-2:] == "pu":
            return self.deleteProccessivePronoun(stem, 2)
        elif stem[-3:] == "nya":
            return self.deleteProccessivePronoun(stem, 3)
        else:
            return {'root': False, 'stem': stem}

    def checkNotCombineSurfix(self, stem):
        if stem[-2:] == "be" and stem[-1] == "i":
            return {'root': True, 'stem': stem}
        elif stem[-2:] == "di" and stem[-2:] == "an":
            return {'root': True, 'stem': stem}
        elif stem[-2:] == "ke" and stem[-1:] == "i":
            return {'root': True, 'stem': stem}
        elif stem[-2:] == "ke" and stem[-3:] == "kan":
            return {'root': True, 'stem': stem}
        elif stem[-2:] == "me" and stem[-2:] == "an":
            return {'root': True, 'stem': stem}
        elif stem[-2:] == "se" and stem[-1:] == "i":
            return {'root': True, 'stem': stem}
        elif stem[-2:] == "se" and stem[-3:] == "kan":
            return {'root': True, 'stem': stem}
        elif stem[-2:] == "te" and stem[-2:] == "an":
            return {'root': True, 'stem': stem}
        else:
            return {'root': False, 'stem': stem}

    def checkDerivationSurfix(self, stem):
        if stem[-1:] == "i":
            return self.deleteDerivationSurfix(stem, 1)
        elif stem[-3:] == "kan":
            return self.deleteDerivationSurfix(stem, 3)
        elif stem[-2:] == "an":
            return self.deleteDerivationSurfix(stem, 2)
        else:
            return {'root': False, 'stem': stem}

    def checkDerivationPrefix(self, stem):
        if stem[:3] == "ber" and stem[3:4] in "aiueo":
            return self.deleteDerivationBerV(stem)
        elif stem[:3] == "ber" and stem[3:4] not in "aiueo":
            return self.deleteDerivationBerCap(stem)
        elif stem == "belajar":
            return self.deleteDerivationBelajar(stem)
        elif stem[:2] == "be":
            return self.deleteDerivationBeC1C2(stem)
        elif stem[3:4] == "b" or stem[3:4] == "f" or stem[3:4] == "v":
            return self.deleteDerivationmemBFV(stem)
        elif stem[:5] == "mempe":
            return self.deleteDerivationmemPE(stem)
        elif stem[3:4] in ["a", "i", "u", "e", "0", "ra", "ri", "ru", "re", "ro"]:
            return self.deleteDerivationmemrVV(stem)
        elif stem[3:4] in "cdjsz":
            return self.deleteDerivationmenCDJSZ(stem)
        elif stem[3:4] in "aiueo":
            return self.deleteDerivationmenVtV(stem)
        elif stem[4:5] in "ghqk":
            return self.deleteDerivationmengGHQK(stem)
        elif stem[4:5] in "aiuo":
            return self.deleteDerivationmengVkV(stem)
        elif stem[4:5] in "aiueo":
            return self.deleteDerivationmenyV(stem)
        elif stem[:4] == "memp":
            return self.deleteDerivationmempA(stem)
        elif stem[:3] == "per" and stem[3:4] in "aiueo":
            return self.deleteDerivationPerV(stem)
        elif stem[:3] == "per" and stem[3:4] not in "aiueor" and stem[5:7] != "er":
            return self.deleteDerivationPerCAP(stem)
        elif stem[:3] == "per" and stem[3:4] not in "aiueo" and stem[5:7] == "er" and stem[7:8] not in "aiueo":
            return self.deleteDerivationPerCAerV(stem)
        elif stem[:3] == "pem" and stem[3:4] in "bfaiueo":
            return self.deleteDerivationPemBFV(stem)
        elif stem[:3] == "pem" and (stem[3:4] == "r" and (stem[4:5] in "aiueo" or stem[3:4] in "aiueo")):
            return self.deleteDerivationPemRVV(stem)
        elif stem[:3] == "pen" and stem[3:4] in "cdjz":
            return self.deleteDerivationPenCDJZ(stem)
        elif stem[:3] == "pen" and stem[3:4] in "aiueo":
            return self.deleteDerivationPenV(stem)
        elif stem[:4] == "peng" and stem[4:5] not in "aiueo":
            return self.deleteDerivationPengC(stem)
        elif stem[:4] == "peng" and stem[4:5] in "aiueo":
            return self.deleteDerivationPengV(stem)
        elif stem[:4] == "peny" and stem[4:5] in "aiueo":
            return self.deleteDerivationPenyV(stem)
        elif stem[:3] == "pel" and stem[3:4] in "aiueo":
            return self.deleteDerivationPelV(stem)
        elif stem[:2] == "pe" and stem[2:3] in "aiueorwylmn" and stem[5:6] in "aiueo":
            return self.deleteDerivationPeCerV(stem)
        elif stem[:2] == "pe" and stem[2:3] in "aiueorwylmn" and stem[3:5] != "er":
            return self.deleteDerivationPeCP(stem)
        elif stem[:3] == "ter" and stem[3:4] != "r" and stem[4:6] == "er":
            return self.deleteDerivationTerC1erC2(stem)
        elif stem[:2] == "pe" and stem[2:3] not in "rwylmn" and stem[3:5] == "er":
            return self.deleteDerivationPeCP(stem)
        return {'root':False, 'stem': stem}

    def deleteDerivationSurfix(self, stem, length):
        stem = stem[:-length]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteProccessivePronoun(self, stem, length):
        return self.deleteDerivationSurfix(stem, length)

    def deleteParticle(self, stem):
        stem = stem[:-3]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteDerivationBerV(self, stem):
        stem = stem[2:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = stem[1:]
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            else:
                return {'root':False, 'stem': stem}

    def deleteDerivationBerCap(self, stem):
        stem = stem[3:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteDerivationBelajar(self, stem):
        return {'root':False, 'stem': 'ajar'}

    def deleteDerivationBeC1C2(self, stem):
        if stem[2:3] not in "rl":
            if len(stem) >= 6:
                if stem[5:6] not in "aiueo" and stem[3:5] == "er":
                    stem = stem[2:]
                    if self.checkStem(stem):
                        return {'root':True, 'stem': stem}
                    return {'root':False, 'stem': stem}
                else:
                    if self.checkStem(stem):
                        return {'root':True, 'stem': stem}
                    return {'root':False, 'stem': stem}
            else:
                if self.checkStem(stem):
                    return {'root':True, 'stem': stem}
                return {'root':False, 'stem': stem}
        else:
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            return {'root':False, 'stem': stem}

    def deleteDerivationTerV(self, stem):
        stem = stem[2:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = stem[1:]
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            return {'root':False, 'stem': stem}

    def deleteDerivationTerCP(self, stem):
        stem = stem[3:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteDerivationTeC1C2(self, stem):
        if (stem[2:3]) != "r":
            if len(stem) >= 6:
                if stem[5:6] not in "aiueo" and stem[3:5] == "er":
                    stem = stem[2:]
                    if self.checkStem(stem):
                        return {'root':True, 'stem': stem}
                    return {'root':False, 'stem': stem}
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteDerivationMeV(self, stem):
        if stem[2:3] in "wyrl":
            if stem[3:4] in "aiueo":
                stem = stem[2:]
                if self.checkStem(stem):
                    return {'root':True, 'stem': stem}
                return {'root':False, 'stem': stem}
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteDerivationmemBFV(self, stem):
        stemTemp = stem
        stem = stem[3:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationmemPE(self, stem):
        return self.deleteDerivationmemBFV(stem)

    def deleteDerivationmemrVV(self, stem):
        stemTemp = stem
        stem = stem[2:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = 'p' + stem[1:]
            stemTemp = stem
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            return {'root':False, 'stem': stemTemp}

    def deleteDerivationmenCDJSZ(self, stem):
        return self.deleteDerivationmemBFV(stem)

    def deleteDerivationmenVtV(self, stem):
        stemTemp = stem
        stem = stem[1:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = 't' + stem[2:]
            stemTemp = stem
            stem = stem[3:]
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            return {'root':False, 'stem': stemTemp}

    def deleteDerivationmengGHQK(self, stem):
        stemTemp = stem
        stem = stem[4:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationmengVkV(self, stem):
        stemTemp = stem
        stem = stem[4:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = 'k' + stem
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            else:
                stem = stem[5:]
                if self.checkStem(stem):
                    return {'root':True, 'stem': stem}
                return {'root':False, 'stem': stemTemp}

    def deleteDerivationmenyV(self, stem):
        stemTemp = stem
        stem = "s" + stem[4:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteDerivationmempA(self, stem):
        stemTemp = stem
        if stem[:1] == "e":
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPerV(self, stem):
        stemTemp = stem
        stem = stem[2:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = stem[1:]
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPerCAP(self, stem):
        stemTemp = stem
        stem = stem[3:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPerCAerV(self, stem):
        return self.deleteDerivationPerCAP(stem)

    def deleteDerivationPemBFV(stem):
        return self.deleteDerivationPerCAP(stem)

    def deleteDerivationPemRVV(self, stem):
        stemTemp = stem
        stem = stem[1:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = "p" + stem[2:]
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPenCDJZ(self, stem):
        return self.deleteDerivationPerCAP(stem)

    def deleteDerivationPenV(self, stem):
        stemTemp = stem
        stem = stem[2:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = "t" + stem[1:]
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPengC(self, stem):
        stemTemp = stem
        stem = stem[4:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPengV(self, stem):
        stemTemp = stem
        stem = stem[4:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        else:
            stem = "k" + stem
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            else:
                if stem[:1] == "e":
                    stem = stem[1:]
                    if self.checkStem(stem):
                        return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPenyV(self, stem):
        stemTemp = stem
        stem = "s" + stem[4:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPelV(self, stem):
        stemTemp = stem
        if stem != "pelajar":
            stem = stem[2:]
            if self.checkStem(stem):
                return {'root':True, 'stem': stem}
            return {'root':False, 'stem': stemTemp}
        else:
            return {'root':True, 'stem': stem}

    def deleteDerivationPeCerV(self, stem):
        stemTemp = stem
        stem = stem[3:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationPeCP(self, stem):
        stemTemp = stem
        stem = stem[2:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stemTemp}

    def deleteDerivationTerC1erC2(self, stem):
        return self.deleteDerivationPeCerV(stem)

    def deleteDerivationPeC1erC2(self, stem):
        return self.deleteDerivationPeCP(stem)

    def deleteDerivationPe(self, stem):
        if stem[2:3] == "w" or stem[2:3] == "y":
            if stem[3:4] in "aiueo":
                stem = stem[2:]
                if self.checkStem(stem):
                    return {'root':True, 'stem': stem}
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def deleteDerivationDi(self, stem):
        stem = stem[2:]
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        return {'root':False, 'stem': stem}

    def process(self, stem):
        if self.checkStem(stem):
            return {'root':True, 'stem': stem}
        result = self.checkLengthStem(stem)
        if result["length"]:
            result = self.checkStemSame(stem)
            if result["root"]:
                return result
            else:
                stem = result["stem"]
                result = self.checkRulePrecedence(stem)
                if result["root"]:
                    return result
                else :
                    stem = result["stem"]
                    result = self.checkParticle(stem)
                    if result["root"]:
                        return result
                    else:
                        stem = result["stem"]
                        result = self.checkProssessivePronoun(stem)
                        if result["root"]:
                            return result
                        else:
                            stem = result["stem"]

                            result = self.checkNotCombineSurfix(stem)
                            if result["root"]:
                                return result
                            else:
                                stem = result["stem"]

                                result = self.checkDerivationSurfix(stem)
                                if result["root"]:
                                    return result
                                else:
                                    stem = result["stem"]

                                    result = self.checkDerivationPrefix(stem)
                                    return result
        else:
            return result
