from typing import Set

from sno.datasource.SCTRelease import SCTRelease


class SCTReleaseWithStated(SCTRelease):

    def __init__(self, release_info, active_concept_hierarchy, all_concepts, stated_hierarchy):
        super().__init__(release_info, active_concept_hierarchy, all_concepts)
        self.stated_hierarchy = stated_hierarchy

    def get_stated_hierarchy(self):
        return self.stated_hierarchy

    def get_stated_hierarchy_release(self):
        return SCTRelease(
            self.get_release_info(),
            self.get_stated_hierarchy(),
            self.get_all_concepts()
        )

    def supports_stated_relationships(self):
        return True
