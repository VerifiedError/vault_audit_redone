from modules.models.models import ContainerData, AuditResult


class VaultAuditor:
    def __init__(self, container_data: ContainerData):
        self.container_data = container_data
        self.expected_labels = container_data.valid_labels

    def audit(self, scanned_labels: list[str]) -> AuditResult:
        scanned_set = set(label.strip() for label in scanned_labels if label.strip())

        matched = scanned_set & self.expected_labels
        unmatched = scanned_set - self.expected_labels
        not_scanned = self.expected_labels - scanned_set

        return AuditResult(
            total_scanned=len(scanned_set),
            matched_labels=matched,
            unmatched_labels=unmatched,
            expected_not_scanned=not_scanned
        )

    def get_summary(self, audit_result: AuditResult) -> dict:
        return {
            'total_containers_in_onsite': len(self.expected_labels),
            'total_scanned': audit_result.total_scanned,
            'matched_count': len(audit_result.matched_labels),
            'unmatched_count': len(audit_result.unmatched_labels),
            'not_scanned_count': len(audit_result.expected_not_scanned)
        }