import os
from typing import List



def potential_file_match(file_names: set, keyword: str) -> bool:
    for file_name in file_names:
        if keyword.lower() in file_name.lower():
            return True
    return False


class LoadLocalRelease:
    @staticmethod
    def find_release_folders(parent_file):
        dir_list = LoadLocalRelease.find_sub(parent_file, [])
        return dir_list

    @staticmethod
    def get_stated_relationships_file(release_directory):
        dir_name = release_directory.abspath()

        if "RF1Release" in dir_name:
            top_level_dir = dir_name[:dir_name.rfind("RF1Release") + len("RF1Release")]
            stated_relationships_dir = os.path.join(top_level_dir, "OtherResources", "StatedRelationships", "")

            stated_rels_dir = os.path.join(stated_relationships_dir)

            if os.path.exists(stated_rels_dir) and os.path.isdir(stated_rels_dir):
                files_list = os.listdir(stated_rels_dir)

                if len(files_list) == 1:
                    return os.path.join(stated_rels_dir, files_list[0])

        return None

    @staticmethod
    def get_release_file_names(release_directories):
        release_names = []

        for directory in release_directories:
            dir_name = directory
            release_name = LoadLocalRelease.extract_release_name(dir_name)
            release_names.append(release_name)

        return release_names

    @staticmethod
    def extract_release_name(dir_name):
        try:
            if "_RF2Release_" in dir_name:
                release_name = dir_name[dir_name.rfind("_RF2Release_"):dir_name.rfind(
                    os.path.sep + "Snapshot" + os.path.sep + "Terminology")]
            elif "RF1" in dir_name:
                if "_RF1Release" in dir_name:
                    release_name = dir_name[dir_name.rfind("RF1Release"):dir_name.rfind(
                        os.path.sep + "Terminology" + os.path.sep + "Content")]
                else:
                    release_name = dir_name[dir_name.rfind("SnomedCT_"):dir_name.rfind(os.path.sep + "RF1")]
            elif "SnomedCT_InternationalRF2_Production" in dir_name:
                release_name = dir_name[
                               dir_name.rfind("InternationalRF2_Production_") + len("InternationalRF2_Production_"):
                               dir_name.rfind(os.path.sep + "Snapshot" + os.path.sep + "")
                               ]
            elif "SnomedCT_InternationalRF2_PRODUCTION" in dir_name:
                release_name = dir_name[
                               dir_name.rfind("InternationalRF2_PRODUCTION_") + len("InternationalRF2_PRODUCTION_"):
                               dir_name.rfind(os.path.sep + "Snapshot" + os.path.sep + "")
                               ]
            else:
                if "Essential Resources" in dir_name:
                    release_name = dir_name[
                                   dir_name.rfind(os.path.sep + "SNOMED_CT_Essential_") + len(
                                       os.path.sep + "SNOMED_CT_Essential_"):
                                   dir_name.rfind(os.path.sep + "Essential Resources")
                                   ]
                else:
                    if "RF2Release" in dir_name:
                        release_name = dir_name[dir_name.rfind("SnomedCT_"):dir_name.rfind(os.path.sep + "RF2Release")]
                    else:
                        release_name = dir_name[
                                       dir_name.rfind("SnomedCT_"):dir_name.rfind(
                                           os.path.sep + "Terminology" + os.path.sep + "Content")
                                       ]

            if "Release_" in release_name:
                release_name = release_name[release_name.rfind("Release_") + len("Release_"):]
            elif "SnomedCT_" in release_name:
                release_name = release_name[release_name.rfind("SnomedCT_") + len("SnomedCT_"):]
            elif "T" in release_name:
                release_name = "INT " + release_name[:release_name.rfind("T")]

            if "RF2" in dir_name:
                release_name += " (RF2)"

            release_name = release_name.replace("_", " ")

            return release_name
        except IndexError as e:
            print("Error getting release name for:", dir_name)
            return ""


    @staticmethod
    def find_sub(directory: str, dir_list: List[str]) -> List[str]:
        if not os.path.isdir(directory):
            return dir_list
        else:
            dir_list = []
            for dirpath, dirnames, filenames in os.walk(directory):
                if 'Snapshot' in dirnames:
                    dir_list.append(dirpath)
            return dir_list



    @staticmethod
    def potential_file_match(file_names, match):
        return any(match.lower() in s.lower() for s in file_names)
