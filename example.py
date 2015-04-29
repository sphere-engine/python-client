import SphereEngineAPI as se

SC = se.SphereEngineAPI('e7a5298eaab2666705871a0d6afaef37')
SP = se.SphereEngineAPI('5f0470b710157fd99a5a001955b010bb13ce7eb5')

test =  'Sphere Compilers'
test += '\n\ttest: ' + SC.compilers.test()[:50] + '...'
test += '\n\tlanguages: ' + SC.compilers.languages()[:50] + '...'
test += '\n\tgetSubmission: ' + SC.compilers.getSubmission(33880429)
test += '\n\tsendSubmission: ' + SC.compilers.sendSubmission('int main() { return 0; }')
test += '\n\nSphere Problems'
test += '\n\ttest: ' + SP.problems.test()
test += '\n\tlanguages: ' + SP.problems.languages()[:50] + '...'
test += '\n\tgetSubmission: ' + SP.problems.getSubmission(962)[:50] + '...'
test += '\n\tsendSubmission: ' + SP.problems.sendSubmission('SEDEMO4', 'int main() { return 0; }')
test += '\n\tproblems: ' + SP.problems.problemsList()[:50] + '...'
test += '\n\tgetProblem: ' + SP.problems.getProblem('SEDEMO4')[:50] + '...'

print test