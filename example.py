import SphereEngineAPI as se

SC = se.SphereEngineAPI({
    'type': 'SC',
    'access_token': 'e7a5298eaab2666705871a0d6afaef37'
    })

SP = se.SphereEngineAPI({
    'type': 'SP',
    'access_token': '5f0470b710157fd99a5a001955b010bb13ce7eb5'
    })

test =  'Sphere Compilers'
test += '\n\ttest: ' + SC.test()[:50] + '...'
test += '\n\tlanguages: ' + SC.languages()[:50] + '...'
test += '\n\tgetSubmission: ' + SC.getSubmission(33916433)
test += '\n\tsendSubmission: ' + SC.sendSubmission({'source': 'int main() { return 0; }'})
test += '\n\nSphere Problems'
test += '\n\ttest: ' + SP.test()
test += '\n\tlanguages: ' + SP.languages()[:50] + '...'
test += '\n\tgetSubmission: ' + SP.getSubmission(962)[:50] + '...'
test += '\n\tsendSubmission: ' + SP.sendSubmission({'problemCode': 'SEDEMO4', 'source': 'int main() { return 0; }'})
test += '\n\tproblems: ' + SP.problems()[:50] + '...'
test += '\n\tgetProblem: ' + SP.getProblem('SEDEMO4')[:50] + '...'

print test