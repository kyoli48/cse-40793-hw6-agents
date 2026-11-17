import unittest
from unittest.mock import patch
import io
import json
import urllib.error
import run_agent


class StyleChecks(unittest.TestCase):
    def test_ollama_request_and_usage(self):
        data = {'done': True, 'done_reason': 'stop',
                'message': {'content': '{"findings": []}'},
                'prompt_eval_count': 31, 'eval_count': 7}
        with patch('run_agent.urllib.request.urlopen', return_value=io.BytesIO(json.dumps(data).encode())) as send:
            result, usage = run_agent.call_model('qwen3:4b', 'review', {'source': 'x'}, 512, 'ollama')
        request = send.call_args.args[0]
        body = json.loads(request.data)
        self.assertEqual(request.full_url, 'http://localhost:11434/api/chat')
        self.assertEqual(body['model'], 'qwen3:4b')
        self.assertFalse(body['stream'])
        self.assertFalse(body['think'])
        self.assertEqual(body['format'], 'json')
        self.assertEqual(body['options']['num_predict'], 512)
        self.assertEqual(result, {'findings': []})
        self.assertEqual(usage['input_tokens'], 31)
        self.assertEqual(usage['output_tokens'], 7)

    def test_ollama_truncation_is_not_a_pass(self):
        data = {'done': True, 'done_reason': 'length', 'message': {'content': '{"findings": []}'}}
        with patch('run_agent.urllib.request.urlopen', return_value=io.BytesIO(json.dumps(data).encode())):
            with self.assertRaisesRegex(ValueError, 'Incomplete Ollama'):
                run_agent.call_model('qwen3', 'review', {}, 10, 'ollama')

    def test_ollama_connection_error_has_setup_hint(self):
        with patch('run_agent.urllib.request.urlopen', side_effect=urllib.error.URLError('refused')):
            with self.assertRaisesRegex(ValueError, 'ollama serve'):
                run_agent.call_model('qwen3', 'review', {}, 100, 'ollama')

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
