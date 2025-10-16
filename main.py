import network
import socket
from machine import Pin, ADC
from time import sleep as delay

#Pin Declaration

html = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zeitmessung</title>
</head>
<body onkeypress="clicks()">
    <div class="titel"><h1>Zeitmessung 🏎️</h1></div>
    <div class="dropdown">
        <button class="button">Wechsle Fahrer</button>
        <div id="dropdown_fahrer"><button id="fahrer_1" class="button" type="button" onclick="anderer_fahrer(1)">Fahrer 1</button>
            <button id="fahrer_2" class="button" type="button" onclick="anderer_fahrer(2)">Fahrer 2</button>
            <button id="fahrer_3" class="button" type="button" onclick="anderer_fahrer(3)">Fahrer 3</button></div></div>
    <div class="button_container"><form><button class="button" type="button" onclick="starte_messung()">Startet die Messung</button><button class="button" type="button" onclick="print_zeitergebnisse()">Drucke deine Zeitergebnisse</button></form></div>
    <div class="messdaten_container">
        <p id="messdaten_live">Live-Zeit:</p>
        <p id="messdaten_titel">Messdaten von ...</p>
        <table id="messtable" style="text-align: center;"><tr><td width="50px"><b>Runde</b></td><td width="200px"><b>Zeit</b></td></tr><tr><td>1</td><td id="messliste">Noch keine Daten</td></tr></table></div>
    <script>
        time_Fahrer1 = [];time_Fahrer2 = [];time_Fahrer3 = [];let min = 0;let sec = 0;let ms = 0;let zeit_str = undefined;let messnummer_fahrer1 = 0;let messnummer_fahrer2 = 0;let messnummer_fahrer3 = 0;
let interval = undefined;const fahrer_titel = document.getElementById("messdaten_titel");const messdaten_live = document.getElementById("messdaten_live");const messtabelle = document.getElementById("messtable");
let click_state = true;let messung_state = false;let one_click;var fahrer = 0;var old_fahrer;anderer_fahrer(1);
function check_photo(){console.log("CHECKPHOT");
    fetch("/check_photo").then(response => response.text()).then(data => {if(data === 'y'){clicks();clicks();}});}
function starte_messung(){
    messung_state = true;clicks();setInterval(check_photo, 10);}
function anderer_fahrer(fahrer_id){
    old_fahrer = fahrer;fahrer = fahrer_id;fahrer_titel.innerText = `Messdaten von Fahrer ${fahrer}:`;
        if(fahrer != old_fahrer){one_click = true;}
    if (fahrer != old_fahrer && localStorage.getItem(`time_Fahrer${fahrer}`) == undefined){leere_werte();new_setup();}
    if (fahrer != old_fahrer && localStorage.getItem(`time_Fahrer${fahrer}`).length > 0){leere_werte();lade_messung();}}
function clicks(){
    console.log("CLICKS");if(click_state && messung_state){interval = setInterval(starte_uhr, 10, true);
        click_state = false; }else if(messung_state){clearInterval(interval);starte_uhr(false);click_state = true;}}
function starte_uhr(uhr_state){
    if(uhr_state){ms++;if(ms%100 == 0){sec++;ms = 0;}if(sec > 0 && sec%60 == 0){min++;sec = 0;}
        messdaten_live.innerText = `Live-Zeit: ${min}m:${sec}s:${ms}ms`;}
    else{zeit_str = `${min}m:${sec}s:${ms}ms`;min = 0;sec = 0;ms = 0;
        if(fahrer == 1){time_Fahrer1.push(zeit_str);localStorage.setItem(`time_Fahrer${fahrer}`, JSON.stringify(time_Fahrer1));}
        if(fahrer == 2){time_Fahrer2.push(zeit_str);localStorage.setItem(`time_Fahrer${fahrer}`, JSON.stringify(time_Fahrer2));}
        if(fahrer == 3){time_Fahrer3.push(zeit_str);localStorage.setItem(`time_Fahrer${fahrer}`, JSON.stringify(time_Fahrer3));}zeit_str = ``;zeige_messung();}}
function zeige_messung(){  
    if(one_click == true){leere_werte();one_click = false;}
    messdaten = JSON.parse(localStorage.getItem(`time_Fahrer${fahrer}`));
    let neueReihe = messtabelle.insertRow();let neueZelle1 = neueReihe.insertCell();let neueZelle2 = neueReihe.insertCell();
    if(fahrer == 1){neueZelle1.innerText = messnummer_fahrer1+1;neueZelle2.innerText = messdaten[messnummer_fahrer1];messnummer_fahrer1++;}
    if(fahrer == 2){neueZelle1.innerText = messnummer_fahrer2+1;neueZelle2.innerText = messdaten[messnummer_fahrer2];messnummer_fahrer2++;
    }if(fahrer == 3){neueZelle1.innerText = messnummer_fahrer3+1;neueZelle2.innerText = messdaten[messnummer_fahrer3]; messnummer_fahrer3++;}}
function lade_messung(){messdaten = JSON.parse(localStorage.getItem(`time_Fahrer${fahrer}`));for (values = 0; values < messdaten.length; values++){
        let neueReihe = messtabelle.insertRow();let neueZelle1 = neueReihe.insertCell();let neueZelle2 = neueReihe.insertCell();neueZelle1.innerText = values+1;neueZelle2.innerText = messdaten[values];}}
function leere_werte(){for(let i = 0; i < messtabelle.rows.length; i=1){messtabelle.deleteRow(1);}}
function new_setup(){let neueReihe = messtabelle.insertRow();let neueZelle1 = neueReihe.insertCell();let neueZelle2 = neueReihe.insertCell();neueZelle1.innerText = 1;neueZelle2.innerText = "Noch keine Daten";
    if(fahrer == 1){messnummer_fahrer1 = 0;}if(fahrer == 2){messnummer_fahrer2 = 0;}if(fahrer == 3){messnummer_fahrer3 = 0;}}
function print_zeitergebnisse(){ window.print();}</script>
            <style>body {zoom: 1.5;}
            .titel {position: absolute;top: -15px;color: #333333;font-family: system-ui;}
            .dropdown {position: absolute;top: 95px;}
            #dropdown_fahrer {display: none;}
            .dropdown:hover #dropdown_fahrer {display: inline;}
            #fahrer_1 {color: #0402fc;}
            #fahrer_2 {color: #fcd728;}
            #fahrer_3 {color: #fc0204;}
            .button_container {position: absolute;top: 60px;}
            .button {color: #ffffff;font-family: system-ui;font-weight: bold;background-color: #333333;border: 4px solid #333333;border-radius: 20px;}
            .button:hover {border: 4px solid #a1a1a1;}
            .messdaten_container {position: absolute;top: 120px;}
            #messdaten_titel {color: #333333;font-family: system-ui;font-weight: bold;font-style: italic;}
            #messdaten_live {color: #333333;font-family: system-ui;font-weight: bold;font-style: italic;}
            table,tr,td {color: #333333;font-family: system-ui;font-style: italic;border: 1px, solid, #333333;border-collapse: collapse;}</style></body></html>"""


# Pin Declaration
pin1 = ADC(Pin(26))

# AP Setup
ap = network.WLAN(network.AP_IF)
ap.config(essid="GoKart", password="password")
ap.active(True)

ip = ap.ifconfig()[0]
address = (ip, 80)

# Show AP-IP address
print(f"IP: {ip}")

# Socket Setup
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.bind(address)
connection.listen(5)
once = True
cval = 100
c = cval
while True:
    conn, addr = connection.accept()
    request = conn.recv(1024)
    val = pin1.read_u16()/19859
    
    if once:
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        conn.send(html)
        conn.close()
        once = False
    
    if "/check_photo" in str(request):
        if val < 1.5:
            response = "y"
            print("CLICKS()")
            print(cval)
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + response)
            conn.close()
            delay(2)

        else:
            response = "n"
            print("End")
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + response)
            conn.close()

    print(val)

    
    







