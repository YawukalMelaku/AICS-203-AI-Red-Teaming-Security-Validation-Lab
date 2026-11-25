"""ICDFA AICS-203 controlled AI workflow simulator. No LLM/API calls or external actions."""
from html import escape

LAB_MARKER = 'ICDFA-DEMO-RESTRICTED-7319'  # Synthetic teaching marker, never a real secret.
TRUSTED_NOTE = 'Evidence review procedure: verify source integrity before approval.'


def evaluate(payload):
    if not isinstance(payload, dict):
        raise ValueError('JSON object required')
    scenario = str(payload.get('scenario', ''))
    mode = str(payload.get('mode', 'baseline'))
    if mode not in ('baseline', 'hardened'):
        raise ValueError('mode must be baseline or hardened')
    token = str(payload.get('lab_token', 'student-demo'))
    role = 'instructor' if token == 'instructor-demo' else 'student'
    text = str(payload.get('text', ''))[:5000]
    document = str(payload.get('document', ''))[:5000]
    operation = str(payload.get('operation', 'read_record'))
    finding, output, authorized = 'none', '', True
    policy_pass = True
    if scenario == 'retrieval':
        if mode == 'baseline' and 'OVERRIDE_TASK:' in document:
            output = document.split('OVERRIDE_TASK:', 1)[1].strip()[:140]
            finding, policy_pass = 'untrusted_document_instruction_obeyed', False
        else:
            output = TRUSTED_NOTE
            finding = 'trusted_instruction_preserved'
    elif scenario == 'disclosure':
        if 'reveal_training_marker' in text.lower():
            if mode == 'baseline' or role == 'instructor':
                output = LAB_MARKER
                if role != 'instructor':
                    finding, policy_pass = 'synthetic_restricted_marker_disclosed', False
            else:
                output = 'Access denied to restricted demonstration record.'
                authorized, finding = False, 'access_control_enforced'
        else:
            output = 'No restricted data requested.'
    elif scenario == 'tool':
        if operation == 'approve_record':
            if mode == 'baseline' or role == 'instructor':
                output = 'SIMULATION ONLY: approval marked in response; no data modified.'
                if role != 'instructor':
                    finding, policy_pass = 'unprivileged_tool_action_simulated', False
            else:
                output = 'Permission denied: approval requires instructor role.'
                authorized, finding = False, 'least_privilege_enforced'
        else:
            output = 'Read-only demonstration operation completed.'
    elif scenario == 'output':
        if mode == 'baseline':
            output = document[:280]
            if '<script' in document.lower() or '<img' in document.lower():
                finding, policy_pass = 'unsafe_unescaped_markup', False
        else:
            output = escape(document[:280], quote=True)
            finding = 'output_encoded'
    else:
        raise ValueError('scenario must be retrieval, disclosure, tool or output')
    return {'scenario': scenario, 'mode': mode, 'simulated_user_role': role,
            'policy_pass': policy_pass, 'authorized': authorized,
            'finding': finding, 'result': output,
            'disclaimer': 'Deterministic offline teaching simulator, not a generative AI model.'}
