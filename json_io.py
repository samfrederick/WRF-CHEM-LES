import json
import sys
import os

def write_emiss_json(chem_opt, config_ozone_precursors=True, fx=None, fy=None, overlap_precursors=None):
    """

    Emissions from the PartMC 'urban plume' test case. 
    The following emissions were not found in the WRF Chem registry, so I
    didn't include them in the dictionary below:

    'E_OLEI': 21.42,  # not found, there is EOLE1 and EOLE2 though
    'E_OLET': 21.42, # not found, there is EOLE1 and EOLE2 though
    'E_AONE': 2.8188, # not found
    'E_ANOL': 19.08 # not found

    """
    # emission rates in mol km^-2 hr^-1
    emiss_species = read_emiss_json(chem_opt)
                
    if config_ozone_precursors and chem_opt == 6:
        if fx is None:
            raise AttributeError('Must pass value of fx to configure precursor emission fields')
        if fy is None:
            raise AttributeError('Must pass value of fy to configure precursor emission fields')
        if overlap_precursors is None:
            raise AttributeError('Must pass boolean value to overlap_precursors')
        
        emiss_species = set_ozone_production_profiles(
            emiss_species, fx=fx, fy=fy, overlap_precursors=overlap_precursors)

    with open('species_emiss_profile_data.json', 'w') as outfile:
        json.dump(emiss_species, outfile, indent=4)


def write_initcond_json(chem_opt, config_ozone_precursors=True, fx=None, fy=None, overlap_precursors=None):
    # initialize with all species set to near-zero values 
    init_species = read_initcond_json(chem_opt)

    if config_ozone_precursors and chem_opt == 6:
        if fx is None:
            raise AttributeError('Must pass value of fx to configure precursor emission fields')
        if fy is None:
            raise AttributeError('Must pass value of fy to configure precursor emission fields')
        if overlap_precursors is None:
            raise AttributeError('Must pass boolean value to overlap_precursors')
        
        init_species = set_ozone_production_profiles(
            init_species, fx=fx, fy=fy, overlap_precursors=overlap_precursors)
    
    with open('species_initcond_profile_data.json', 'w') as outfile:
        json.dump(init_species, outfile, indent=4)

def read_emiss_json(chem_opt):
    # Read archival copy of profile emissions json file        
    with open(os.path.join(os.getcwd(), 'profile-jsons', f'chemopt{chem_opt}', 'species_emiss_profile_data.json'), 'r') as infile:    
        data = json.load(infile)
    return data

def read_initcond_json(chem_opt):
    # Read archival copy of profile initial condition json file
    with open(os.path.join(os.getcwd(), 'profile-jsons', f'chemopt{chem_opt}', 'species_initcond_profile_data.json'), 'r') as infile:    
        data = json.load(infile)
    return data


def set_ozone_production_profiles(species_dict, fx, fy, overlap_precursors=False):
    """Configure precursor emissions for ozone production

    """
    voc_keys = ['E_ALD2', 'E_HCHO', 'E_ETH', 'E_TOL', 
                    'E_XYL', 'E_PAR', 'E_ISOP', 'E_CH3OH']
    
    if not all([name.startswith('E_') for name in species_dict.keys()]):
        voc_keys = [key.replace('E_', '').lower() for key in voc_keys]
    
    for species in species_dict:
        species_dict[species]['profile_fx'] = fx
        species_dict[species]['profile_fy'] = fy
        species_dict[species]['profile_phase_shift'] = False

    if not overlap_precursors:
        for species in voc_keys:
            species_dict[species]['profile_fx'] = fx
            species_dict[species]['profile_fy'] = fy
            species_dict[species]['profile_phase_shift'] = True
        
    return species_dict



if __name__ == '__main__':
    # Access the command-line argument passed from the Bash script
    chem_opt = int(sys.argv[1])
    write_emiss_json(chem_opt, config_ozone_precursors=True, 
                     fx=1, fy=1, overlap_precursors=False)
    write_initcond_json(chem_opt, config_ozone_precursors=True, 
                        fx=1, fy=1, overlap_precursors=False)
