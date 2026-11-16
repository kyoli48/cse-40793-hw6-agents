import unittest
import run_agent


class StyleChecks(unittest.TestCase):
    def test_comments_and_strings_are_not_functions(self):
        self.assertEqual(run_agent.deterministic('# def badName():\ntext = "def badName():"\n', {'S003','S004'}), [])

    def test_known_violations(self):
        findings = run_agent.deterministic('def badName():\n    return 1  \n', {'S001','S003','S004'})
        self.assertEqual({(f['rule_id'],f['line']) for f in findings}, {('S001',2),('S003',1),('S004',1)})

    def test_judge_evidence_must_be_real(self):
        with self.assertRaises(ValueError):
            run_agent.validate([dict(rule_id='S999',line=1,evidence='x',message='x',suggestion='x')], ['x'], {'S001'})
        with self.assertRaises(ValueError):
            run_agent.validate([dict(rule_id='S001',line=1,evidence='invented',message='x',suggestion='x')], ['x'], {'S001'})


if __name__ == '__main__':
    unittest.main()
