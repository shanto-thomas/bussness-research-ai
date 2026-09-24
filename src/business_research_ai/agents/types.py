from enum import StrEnum


class AgentType(StrEnum):
    ORCHESTRATOR = "orchestrator"
    MARKET = "market"
    COMPETITOR = "competitor"
    CUSTOMER = "customer"
    PRICING = "pricing"
    FINANCE = "finance"
    LEGAL = "legal"
    TECHNOLOGY = "technology"
    SYNTHESIS = "synthesis"
    REPORT = "report"