# Control: CC6.1 (SOC 2)
# Framework: soc-2
# Description: Logical access controls protect information assets from security events.
# Evidence event_type: iam_identity_snapshot

package compliance.soc2.cc6_1

default allow := false

# Condition 1: identity must be authenticated.
deny[msg] {
	not input.payload.authenticated
	msg := {
		"control_id": "cc6_1",
		"reason": "identity is not authenticated",
		"resource": input.resource_id,
		"severity": "high",
	}
}

# Condition 2: privileged identities require MFA.
deny[msg] {
	input.payload.privileged
	not input.payload.mfa_enabled
	msg := {
		"control_id": "cc6_1",
		"reason": "privileged identity lacks MFA enforcement",
		"resource": input.resource_id,
		"severity": "critical",
	}
}

# Condition 3: role assignment must carry an approval ticket reference.
deny[msg] {
	input.payload.role
	not input.payload.approval_ticket
	msg := {
		"control_id": "cc6_1",
		"reason": "role assignment lacks documented approval",
		"resource": input.resource_id,
		"severity": "medium",
	}
}

# Condition 4: service accounts must not have console credentials.
deny[msg] {
	input.payload.identity_type == "service"
	input.payload.console_password_set
	msg := {
		"control_id": "cc6_1",
		"reason": "service account has interactive console credentials",
		"resource": input.resource_id,
		"severity": "high",
	}
}
