import os
import sys
import numpy as np
import folium
import json


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




def create_fcps_and_pois_map(fcp_json_d, pois_d, fps_pois_ptf):
    '''
    plotting map using folium

    '''
    lon = 12.00
    lat = 40.00
    m = folium.Map(location = (lat, lon),
                   control_scale = True, 
                   zoom_start = 5)

    forecast_points = folium.FeatureGroup(name="Forecast Points PTF", control=True).add_to(m)
    forecast_points_jabba = folium.FeatureGroup(name="Forecast Points Bernardi", control=True).add_to(m)
    points_of_interest = folium.FeatureGroup(name="Points of Interest", show=True).add_to(m)
    points_of_interest_associated = folium.FeatureGroup(name="Points of Interest associated", control=True).add_to(m)

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
            tooltip=f"{name}: {coords[0]}, {coords[1]}",
            popup=f"{name} {coords[0]}, {coords[1]}"
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
            tooltip=f"POI {name}: {coords[0]}, {coords[1]}",
            popup=f"{name} {coords[0]}, {coords[1]}"
                    ).add_to(points_of_interest)

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
            tooltip=f"{name_fcp}: {coords[0]}, {coords[1]}",
            popup=f"{name_fcp}: {coords[0]}, {coords[1]}"
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
        &nbsp; Forecast Points Bernardi &nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
        &nbsp; Points of Interest associated &nbsp; <i class="fa fa-circle fa-lg" style="color:green"></i><br>
        &nbsp; Points of Interest NEAM &nbsp; <i class="fa fa-circle" style="color:green"></i><br>
    </div>
    '''

    # Add the legend to the map
    m.get_root().html.add_child(folium.Element(legend_html))


def load_fcp_full_list_json(filename):
    '''
    json file from jabba service from fabrizio.b
    <class 'dict'> dict_keys(['meta', 'data'])
    list ['meta']['data'][0] =
    {'id': 1, 'name': 'KATAKOLO', 'state': 'GREECE', 
    'lat': 37.644, 'lon': 21.323, 'depth': 0, 
    'fk_it_region': None, 'fk_fcp_status': 11, 
    'modified': '2021-10-14 07:38:39', 
    'calc_lat': 37.644, 'calc_lon': 21.323, 'calc_depth': -44.44921875}
    '''

    if filename is not None:
        filename = filename

    with open(filename, 'r', encoding='utf-8') as fcp_file:
        txt = json.load(fcp_file)
        n_fcp = txt['meta']['total']
        # for i in range(n_fcp):
        #     if txt['data'][i]['state'] == 'ITALY':
        #         print(txt['data'][i]['name'], txt['data'][i]['fk_fcp_status'])

    keys = [txt['data'][item]['name'] for item in range(n_fcp)]
    values = [(txt['data'][item]['lon'], txt['data'][item]['lat']) for item in range(n_fcp)]
    return dict(zip(keys, values))


def load_pois(filename):
    '''
    pois used in ptf (pois.npy file) 
    '''
    pois_ptf = np.load(filename, allow_pickle=True).item()
    # print(pois_ptf.keys())
    keys = pois_ptf['name']
    values = [(lon, lat) for (lon, lat) in zip(pois_ptf['lon'], pois_ptf['lat'])]
    return dict(zip(keys, values))


def main():

    # create dictionary from json file from fabrizio.b jabba service
    fcp_json_f = os.path.join('data', 'fcp_full_list_jabba.json')
    fcp_json_d = load_fcp_full_list_json(fcp_json_f)

    # create dictionary from npy file used in ptf
    pois_f = os.path.join('data', 'pois.npy')
    pois_d = load_pois(pois_f)

    # fcp and pois association
    pois_to_fcp_f = os.path.join('data', 'pois_to_fcp.npy')
    fps_pois_ptf = np.load(pois_to_fcp_f, allow_pickle=True).item()

    # create map
    create_fcps_and_pois_map(fcp_json_d, pois_d, fps_pois_ptf)

if __name__ == "__main__":
    main()
