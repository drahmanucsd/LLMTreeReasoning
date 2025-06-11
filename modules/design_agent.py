import re
from typing import List, Dict, Any

class DesignAgent:
    """
    Generates a file/folder structure plan from a merged plan list.

    Each high-level step is mapped to a Python module under `src/` and a corresponding test under `tests/`.
    Returns a nested dict representing the tree. Leaf files have value None.
    """

    def __init__(self, project_name: str = "project"):
        self.project_name = project_name

    def _sanitize(self, text: str) -> str:
        """
        Convert a descriptive step text into a filesystem-friendly slug.
        """
        slug = text.strip().lower()
        # replace non-alphanumeric with underscores
        slug = re.sub(r"[^a-z0-9]+", "_", slug)
        # collapse multiple underscores
        slug = re.sub(r"_+", "_", slug).strip("_")
        return slug or "step"

    def plan(self, merged_plan: List[str]) -> Dict[str, Any]:
        """
        Build a nested dict representing:
        project_name/
          README.md
          src/
            <step_slug>.py
          tests/
            test_<step_slug>.py

        :param merged_plan: Ordered list of high-level plan steps.
        :return: Nested dict mirror of the folder/file tree.
        """
        tree: Dict[str, Any] = {}
        # root README
        tree["README.md"] = None

        # src folder
        src_tree: Dict[str, None] = {}
        for step in merged_plan:
            slug = self._sanitize(step)
            filename = f"{slug}.py"
            src_tree[filename] = None
        tree["src"] = src_tree

        # tests folder
        test_tree: Dict[str, None] = {}
        for step in merged_plan:
            slug = self._sanitize(step)
            test_name = f"test_{slug}.py"
            test_tree[test_name] = None
        tree["tests"] = test_tree

        return {self.project_name: tree}
