import agents


def test_list_agent_roles():
    expected_roles = [
        "Senior Market Research Specialist",
        "Strategic Business Analyst",
        "Senior Investment Report Writer",
    ]
    assert hasattr(agents, "list_agent_roles"), (
        "Function list_agent_roles does not exist in agents"
    )
    assert agents.list_agent_roles() == expected_roles, (
        "The roles returned do not match the expected list of roles"
    )
