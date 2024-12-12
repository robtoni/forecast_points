import os
import sys
import numpy as np
import folium
import json


def print_pois_to_fcp(pois_to_fcp_ptf):
    '''
    '''
    with open('pois_to_fcp_ptf.txt', 'w') as f:
        for k, v in pois_to_fcp_ptf.items():
            ind = sorted([int(item[3:].lstrip('0')) for item in v[0]])
            ind_str = ' '.join(str(item) for item in ind)
            #coords = sorted([float(item) for item in v[1]])
            #coords_str = ' '.join(str(item) for item in coords)
            f.write(f"{k} {ind_str}\n")

def print_pois_neamthm18(pois_d):
    '''
    '''
    with open('pois_neamthm18.txt', 'w') as f:
        for k, v in pois_d.items():
            #ind = sorted([int(item[3:].lstrip('0')) for item in v[0]])
            #ind_str = ' '.join(str(item) for item in ind)
            #coords = sorted([float(item) for item in v[1]])
            #coords_str = ' '.join(str(item) for item in coords)
            f.write(f"{k} {v}\n")


def list_comparison():
    '''
    '''
    # fps_pois_ptf_str = []
    # for k, v in fps_pois_ptf.items():
    #     ind = sorted([int(item[3:].lstrip('0')) for item in v[0]])
    #     ind_str = ' '.join(str(item) for item in ind)
    #     coords = sorted([float(item) for item in v[1]])
    #     coords_str = ' '.join(str(item) for item in coords)
    #     #print(f"{k} {ind_str}")
    #     fps_pois_ptf_str.append(f"{k} {coords_str} {ind_str}")

    # fps_pois_ptf_tot = len(fps_pois_ptf_str)
    # #sys.exit()
    # corrs = set(fps_pois_str).intersection(fps_pois_ptf_str)
    # diffs = set(fps_pois_str).difference(fps_pois_ptf_str)
    # diffs2 = set(fps_pois_ptf_str).difference(fps_pois_str)

    # print(f"Corresponding: {len(corrs)}/{len(fps_pois_ptf_str)}")
    # print(f"Missing: {len(diffs)}")


    # # file from manual association (fabrizio.r alessio)
    # with open('FP_POI.dat', 'r') as f:
    #     fps_pois_str = []
    #     for line in f.readlines():
    #         tmp = line.split()
    #         name = tmp[0]
    #         ind = sorted([int(item) for item in tmp[1:]])
    #         ind_str = ' '.join(str(item) for item in ind)
    #         fps_pois_str.append(f"{name} {ind_str}")

    # fps_pois_tot = len(fps_pois_str)
    # #print(fps_pois_str)

    # for diff in diffs:
    #     print(diff)
    # print()
    # for diff in diffs2:
    #     print(diff)
    # print()
    # for fp_pois_ptf_str in fps_pois_ptf_str:
    #     print(fp_pois_ptf_str)
    # print()
    # for fp_pois_str in fps_pois_str:
    #     print(fp_pois_str)




def create_fcps_and_pois_map(fcp_json_d, pois_d, fps_pois_ptf, ptf_stations_d):
    '''
    plotting map using folium

    '''
    lon = 12.00
    lat = 40.00
    m = folium.Map(location = (lat, lon),
                   control_scale = True, 
                   zoom_start = 5)

    forecast_points = folium.FeatureGroup(name="Forecast Points PTF", control=True, show=False).add_to(m)
    forecast_points_jabba = folium.FeatureGroup(name="Forecast Points Tsuface", control=True).add_to(m)
    points_of_interest = folium.FeatureGroup(name="Points of Interest", control=True, show=False).add_to(m)
    points_of_interest_associated = folium.FeatureGroup(name="Points of Interest associated", control=True, show=False).add_to(m)
    ptf_stations = folium.FeatureGroup(name="Sea-level Stations Tsuface", control=True).add_to(m)

    # plotting all fcp
    for name, coords in fcp_json_d.items():
        folium.CircleMarker(
            location = (coords[1], coords[0]),
            radius=6,
            color='blue',
            fill=True,
            #fill_opacity=0.6,
            weight=2,
            #icon = folium.Icon("blue"),
            tooltip=f"{name}: {coords[1]}, {coords[0]}",
            popup=f"{name} {coords[1]}, {coords[0]}"
                    ).add_to(forecast_points_jabba)

    # plotting all pois
    for name, coords in pois_d.items():
        folium.CircleMarker(
            location = (coords[1], coords[0]),
            radius=6,
            color='green',
            fill=True,
            weight=2,
            #icon = folium.Icon("blue"),
            tooltip=f"POI {name}: {coords[1]}, {coords[0]}",
            popup=f"{name} {coords[1]}, {coords[0]}"
                    ).add_to(points_of_interest)

    # # plotting ptf sea-level stations
    # for name_st, coords_st in ptf_stations_d.items():
    #     folium.CircleMarker(
    #         location = (coords_st[1], coords_st[0]), 
    #         radius=8,
    #         color='black',
    #         fill=True,
    #         weight=2,
    #         #icon = folium.Icon("red"),
    #         tooltip=f"{name_st}: {coords_st[1]}, {coords_st[0]}",
    #         popup=f"{name_st}: {coords_st[1]}, {coords_st[0]}"
    #                 ).add_to(ptf_stations)
    # plotting ptf sea-level stations
    for name_st, coords_st in ptf_stations_d.items():
        folium.Marker(
            location = (coords_st[1], coords_st[0]), 
                       icon=folium.Icon(
                       color='white',
                       icon_color='blue',
                       icon='line-chart',
                       prefix='fa'),
            tooltip=f"{name_st}: {coords_st[1]}, {coords_st[0]}",
            popup=f"{name_st}: {coords_st[1]}, {coords_st[0]}"
                    ).add_to(ptf_stations)


    # plotting all fcp with corresponding pois
    for name_fcp, value in fps_pois_ptf.items():
        pois = value[0]
        coords = value[1]
        # print(name_fcp, coords, pois)
        folium.CircleMarker(
            location = (coords[1], coords[0]), 
            radius=10,
            color='red',
            fill=True,
            weight=2,
            #icon = folium.Icon("red"),
            tooltip=f"{name_fcp}: {coords[1]}, {coords[0]}",
            popup=f"{name_fcp}: {coords[1]}, {coords[0]}"
                    ).add_to(forecast_points)
        
        for poi in pois:
            if poi in pois_d.keys():
                folium.CircleMarker(
                    location = (pois_d[poi][1], pois_d[poi][0]), 
                    radius=10,
                    color='green',
                    fill=True,
                    weight=2,
                    #icon = folium.Icon("green"),
                    tooltip=f"{poi}: {name_fcp}",
                    popup=f"{poi}: {pois_d[poi][0]}, {pois_d[poi][1]} {name_fcp}"
                            ).add_to(points_of_interest_associated)
            else:
                continue
                # print(f" - No poi {poi}")

    create_legend(m)
    folium.LayerControl().add_to(m)
    m.save("index.html")


def create_legend(m):
    # Define the legend's HTML
    legend_html = '''
    <div style="position: fixed; 
        bottom: 50px; left: 50px; width: 240px; height: 140px; 
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color:white; opacity: 0.85;">
        &nbsp; <b>Legend</b> <br>
        &nbsp; Forecast Points PTF &nbsp; <i class="fa fa-circle" style="color:red"></i><br>
        &nbsp; Forecast Points Tsuface &nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
        &nbsp; Points of Interest associated &nbsp; <i class="fa fa-circle fa-lg" style="color:green"></i><br>
        &nbsp; Points of Interest NEAM &nbsp; <i class="fa fa-circle" style="color:green"></i><br>
        &nbsp; Sea-level Stations Tsuface &nbsp; <i class="fa fa-line-chart fa-lg" style="color:blue"></i><br>
    </div>
    '''

    # Add the legend to the map
    m.get_root().html.add_child(folium.Element(legend_html))


def load_tsuface_fcp(filename):
    '''
    json file from jabba service from fabrizio.b
    <class 'dict'> dict_keys(['meta', 'data'])
    list ['meta']['data'][0] =
    {'id': 1, 'name': 'KATAKOLO', 'state': 'GREECE', 
    'lat': 37.644, 'lon': 21.323, 'depth': 0, 
    'fk_it_region': None, 'fk_fcp_status': 11, 
    'modified': '2021-10-14 07:38:39', 
    'calc_lat': 37.644, 'calc_lon': 21.323, 'calc_depth': -44.44921875}

    json from tsuface
    {'id': 1, 'name': 'KATAKOLO', 'state': 'GREECE', 'lat': 37.644, 'lon': 21.323, 'depth': 0, 
    'fk_it_region': None, 'fk_fcp_status': 11, 'modified': '2021-10-14 07:38:39', 
    'calc_lat': 37.644, 'calc_lon': 21.323, 'calc_depth': -44.44921875, 'status': {'id': 11, 'name': 'official'}}
    '''

    if filename is not None:
        filename = filename

    with open(filename, 'r', encoding='utf-8') as tsuface_fcp_file:
        fcp_list = json.load(tsuface_fcp_file)
        # n_st = len(fcp_list)
        fcps_d = dict()
        for ic, fcp_d in enumerate(fcp_list):
            if fcp_d['lat'] is not None or fcp_d['lon'] is not None :
                print(fcp_d['name'], fcp_d['lon'], fcp_d['lat'])
                fcps_d[fcp_d['name']] = (float(fcp_d['lon']), float(fcp_d['lat']))
                # ic += 1
    
    # print(f"{ic}/{n_st}")
    return fcps_d



    # with open(filename, 'r', encoding='utf-8') as fcp_file:
    #     txt_fcp = json.load(fcp_file)
    #     print(txt_fcp[0])
    #     sys.exit()
    #     n_fcp = txt_fcp['meta']['total']

    # keys = [txt_fcp['data'][item]['name'] for item in range(n_fcp)]
    # values = [(txt_fcp['data'][item]['lon'], txt_fcp['data'][item]['lat']) for item in range(n_fcp)]
    # return dict(zip(keys, values))


def load_pois(filename):
    '''
    pois used in ptf (pois.npy file) 
    '''
    pois_ptf = np.load(filename, allow_pickle=True).item()
    # print(pois_ptf.keys())
    keys = pois_ptf['name']
    values = [(lon, lat) for (lon, lat) in zip(pois_ptf['lon'], pois_ptf['lat'])]
    return dict(zip(keys, values))


def load_tsuface_stations(filename):
    '''
    json file from tsuface
    {'id': 118741, 'fk_fcp': 11211, 'fk_sensor_type': 71, 'station': 'aigi', 'channel': 'UTZ', 'network': 'ZZ', 'location': '01', 
     'start_time': '2021-05-17 18:03:14', 'end_time': '2999-12-31 00:00:00', 'modified': '2021-05-17 16:03:13', 'samples': 1, 
     'seconds': 60, 'instr_lat': 38.2571, 'instr_lon': 22.0769, 'instr_depth': None, 'sensor_full': {'id': 71, 'name': 'rad'}, 'sensor': 'rad', 
     'scnl_downloadinfo': {'id': 1351, 'fk_scnl': 118741, 'provider': 'IOC', 'download_id': None, 'transfer_file_name': None, 'country_code': 'HEL'}, 
     'fcp': {'id': 11211, 'name': 'AIGIO', 'state': 'GREECE', 'lat': 38.26, 'lon': 22.08, 'depth': 0, 
     'fk_it_region': None, 'fk_fcp_status': 11, 'modified': '2021-10-14 07:38:39', 'calc_lat': 38.2583, 'calc_lon': 22.0917, 'calc_depth': -76.2109375, 'status': 'official'}, 
     'neam_area': True, 'isOpen': True}
    '''
    with open(filename, 'r', encoding='utf-8') as ptf_st_file:
        stations_list = json.load(ptf_st_file)
        # n_st = len(stations_list)
        stations_d = dict()
        for ic, stat_d in enumerate(stations_list):
            if stat_d['instr_lat'] is not None or stat_d['instr_lon'] is not None :
                print(stat_d['station'], stat_d['instr_lon'], stat_d['instr_lat'])
                stations_d[stat_d['station']] = (float(stat_d['instr_lon']), float(stat_d['instr_lat']))
                # ic += 1
    
    # print(f"{ic}/{n_st}")
    return stations_d


def main():

    # create dictionary from json file from fabrizio.b jabba service
    # fcp_json_f = os.path.join('data', 'fcp_full_list_jabba.json')
    fcp_json_f = os.path.join('data', 'FCPs_data_export_1734028135028.json')
    fcp_json_d = load_tsuface_fcp(fcp_json_f)

    # create dictionary from npy file used in ptf
    pois_f = os.path.join('data', 'pois.npy')
    pois_d = load_pois(pois_f)

    # fcp and pois association
    pois_to_fcp_f = os.path.join('data', 'pois_to_fcp.npy')
    pois_to_fcp_ptf = np.load(pois_to_fcp_f, allow_pickle=True).item()
 
    # ptf stations
    ptf_stations_f = os.path.join('data', 'stations_data_export_2024.12.12.json')
    ptf_stations_d = load_tsuface_stations(ptf_stations_f)

    # print on screen pois associated to fcp in ptf
    print_pois_to_fcp(pois_to_fcp_ptf)
    print_pois_neamthm18(pois_d)

    # create map
    create_fcps_and_pois_map(fcp_json_d, pois_d, pois_to_fcp_ptf, ptf_stations_d)

if __name__ == "__main__":
    main()
