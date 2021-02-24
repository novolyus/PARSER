from netmiko import ConnectHandler
import pprint
from device_test import devices
from jinja2 import Environment, FileSystemLoader 
import smtplib, email
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase



liste_parsed = []
recipients = ['franqueza@un.org', 'abella@un.org']


def connect_device(device_name, int_list):
    switch = {
        'device_type':'cisco_nxos',
        'host':device_name,
        'username':'shownet', 
        'password':'234$Snwrk!!',
        'port':22,
        'verbose':True
    }
    print('*'*50 + '\n')
    print(f'opening connection to... {device_name} \n')
    print('sending commnands\n\n')
    net_connect = ConnectHandler(**switch)
    list_outs = []
    for intf in int_list:
        output = net_connect.send_command(f'show interface {intf}', use_textfsm = True)
        list_outs.append(output)
    net_connect.disconnect()
    return (list_outs)



def parse_output(raw_result):
  parsed_result = []  
  for intefs1 in origin:
    for d in intefs1:
      new_dict = {'int_name':d['interface'],
                  'status': d['link_status'],
                  'descr':d['description'], 
                  'mac':d['bia'],
                  'crc':d['crc'],
                  'in_err':d['input_errors'],
                  'out_err':d['output_errors']}
      parsed_result.append(new_dict)
  return(parsed_result)  
     


def create_template(parsing_devices,template_name): 
    ENV = Environment(loader = FileSystemLoader('.'))    
    template = ENV.get_template("template.j2")
    templated_device = (template.render(parsing_devices = parsing_devices))
    with open(template_name,  "w") as file:
        file.write(templated_device)
        file.close



def errors_found(liste):
    faulty_device = {}
    list_of_faults = []
    fake = False
    for device in liste:
        name = list(device.keys())[0]
        for chungo in device.values():
           error_list = []
           for int_names in chungo:
               dict_errors = {}
               beacon = False
               for k,v in  int_names.items():
                   if k == 'int_name':
                       intf = {k:v}
                       dict_errors.update(intf) 
                   if k == 'status' and v != 'up':
                       beacon = True
                       err1 = {k:v}
                       dict_errors.update(err1)
                   if k == 'crc' and v != '0':
                       beacon = True
                       err2 = {k:v}
                       dict_errors.update(err2)
                   if k == 'in_err' and v != '0':
                       beacon = True
                       err3 = {k:v}
                       dict_errors.update(err3)
                   if k == 'out_err' and v != '0':
                       beacon = True
                       err4 = {k:v}
                       dict_errors.update(err4)                    
               if beacon:
                  error_list.append(dict_errors)
           if len(error_list) !=0:
              faulty_device = {name:error_list}
              list_of_faults.append(faulty_device)
    if len(list_of_faults) != 0:
        return(list_of_faults)
    else:
        fake = True
        return(fake)                   





for device in devices:
    die_liste = []
    brad_pitt = {}
    for interfaces in device.values():
        for ethernet in interfaces:
            ints = interfaces[ethernet]
            for inte in ints:
                die_liste.append(inte)
    device_liste = list(device.keys())[0]
    origin = connect_device(device_liste, die_liste) 
    parsed_output = parse_output(origin)
    brad_pitt = {device_liste:parsed_output}
    liste_parsed.append(brad_pitt)
    
create_template(liste_parsed, 'template.html') 

defined_errors = errors_found(liste_parsed)

print(defined_errors)



########################################
###     THE LOOP OF THE DEATH     ######
###   A TEMPLATE FOR THE FUTURE   ######
###   by: Sylvester Netmikoni     ######
########################################    
# def errors_found(liste)::
#     for device in parsing_devices:
#         for name in device:
#             print(name)
#             for chungo in device.values():
#                 print(chungo)
#                 for int_names in chungo:
#                     print(int_names)
#                     for k,v in  int_names.items():
#                         print(k + '\n')
#                         print(v)
