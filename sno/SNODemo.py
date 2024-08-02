import os
from pathlib import Path

from core.abn.node.PartitionedNode import PartitionedNode
from core.abn.node.SimilarityNode import SimilarityNode
from core.abn.node.SinglyRootedNode import SinglyRootedNode
from sno.datasource.SCTReleaseInfo import SCTReleaseInfo
from sno.load.LoadLocalRelease import LoadLocalRelease
from sno.load.RF2ReleaseLoader import RF2ReleaseLoader


def main():
    input_directory = Path("G:/Ontology/SNO")
    print("Loading")
    default_cat = False

    if input_directory.is_dir():
        subfiles = input_directory.iterdir()

        for file in subfiles:
            if file.is_dir():
                print("Find file:", file.absolute())
                # dir_list = LoadLocalRelease.find_release_folders(file)
                dir_list = ['G:\Ontology\SNO\SnomedCT_InternationalRF2_PRODUCTION_20210731T120000Z\Snapshot\Terminology']
                for t in dir_list:
                    print("dir", t)

                release_names = LoadLocalRelease.get_release_file_names(dir_list)
                for t in release_names:
                    print("release", t)

                release_name = release_names[0]
                try:
                    rf2_importer = RF2ReleaseLoader()

                    dir_file = dir_list[0]
                    release = rf2_importer.load_local_snomed_release(
                        dir_file,
                        SCTReleaseInfo(dir_file, release_name),
                    )

                    valid_roots = sorted(release.get_hierarchies_with_attribute_relationships(),
                                         key=lambda x: x.get_name())

                    for root in valid_roots:
                        root_concept = release.get_concept_from_id(root.get_id())
                        print("root_concept.getName() =", root_concept.get_name())

                    concept_id = 49601007
                    opt_concept = release.get_concept_from_id(concept_id)
                    print("opt_concept.getName() =", opt_concept.get_name())


                    concept_id = 404684003
                    opt_concept = release.get_concept_from_id(concept_id)
                    print("opt_concept.getName() =", opt_concept.get_name())

                    hier = release.get_concept_hierarchy()

                    print("------------ checking get_descendant_hierarchy_within_distance ----------------")
                    concept_id = 106063007
                    opt_concept = release.get_concept_from_id(concept_id)
                    print("opt_concept.getName() =", opt_concept.get_name())
                    concept_set = hier.get_descendant_hierarchy_within_distance(opt_concept, 1).get_nodes()
                    print("------------ count: ", len(concept_set))
                    for node in concept_set:
                        print(node.get_name())

                    print("------------ checking get_children ------------")
                    print("opt_concept.getName() =", opt_concept.get_name())
                    concept_set = hier.get_children(opt_concept)
                    print("------------ count: ",  len(concept_set))
                    for node in concept_set:
                        print(node.get_name())

                    print("------------ checking count_descendants ------------")
                    print("------------ count of descendants: ", hier.count_descendants(opt_concept))

                    concept_id = 301095005
                    opt_concept = release.get_concept_from_id(concept_id)
                    # hier = release.get_concept_hierarchy()
                    # anc_hier= hier.get_ancestor_hierarchy([opt_concept])

                    print("------------ checking get_ancestors ------------")
                    for node in hier.get_ancestors({opt_concept}):
                        print(node.get_name())

                    print("------------ checking get_siblings ------------")

                    opt_concept = release.get_concept_from_id(concept_id)
                    print("opt_concept.getName() =", opt_concept.get_name())
                    for node in hier.get_siblings(opt_concept):
                        print(node.get_name())

                    print("------------ checking get_strict_siblings ------------")
                    print("opt_concept.getName() =", opt_concept.get_name())
                    for node in hier.get_strict_siblings(opt_concept):
                        print(node.get_name())

                    print("------------ checking get_all_paths_to ------------")
                    paths = hier.get_all_paths_to(opt_concept)
                    for path in paths:
                        print('->'.join([x.get_name() for x in path]))

                    concept_id = 301095005
                    opt_concept_1 = release.get_concept_from_id(concept_id)

                    concept_id = 106063007
                    opt_concept_2 = release.get_concept_from_id(concept_id)

                    print("------------ checking is_ancestor_of ------------")
                    print(hier.is_ancestor_of(opt_concept_2, opt_concept_1))

                    print("------------ checking is_descendant_of ------------")
                    print(hier.is_descendant_of(opt_concept_1, opt_concept_2))

                    print("------------ checking get_all_longest_path_depths ------------")
                    print(len(hier.get_all_longest_path_depths()))

                    print("------------ checking lowest_common_ancestors ------------")

                    concept_id = 254206003
                    opt_concept_2 = release.get_concept_from_id(concept_id)
                    for node in hier.lowest_common_ancestors(set([opt_concept_1, opt_concept_2])):
                        print(node.get_name())

                    print("------------ checking is_descendant_of ------------")

                    concept_id = 27550009
                    opt_concept_3 = release.get_concept_from_id(concept_id)

                    print(hier.is_descendant_of(opt_concept_1, opt_concept_3))
                    print(hier.is_descendant_of(opt_concept_2, opt_concept_3))



                    print("------------ checking get_topological_descendant_list_within_distance ----------------")
                    concept_id = 27550009
                    opt_concept = release.get_concept_from_id(concept_id)
                    print("opt_concept.getName() =", opt_concept.get_name())
                    result_list = hier.get_topological_descendant_list_within_distance(opt_concept, 2)
                    print("------------ count: ", len(result_list))
                    for result in result_list[-3:]:
                        print(result.get_node().get_name())
                        print(result.get_depth())



                except IOError as e:
                    # TODO: write error...
                    pass


if __name__ == "__main__":
    main()
