import sys
import os
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

#Code python pour générer le code html de l'oscilloscope virtuel
#Sous license CC BY-SA 4.0 international
#Par Julien Rosssignol
#Requis: pandas, numpy and pyxlsb

def generateScope(filepath, scale, colors, textStyle, applet):
    if(not filepath.exists()):
        print(f"Le fichier {filepath.name} n'existe pas")
        return
    
    #Lit le fichier excel
    scopeDF = pd.read_excel(filepath, "Oscilloscope")
    
    i = 0;
    pointCode = ""
    switchCode = ""
    textCode = ""
    circuitCode = ""
    helperCode = ""
    
    #Pour chaque ligne du excel, génère le point, le texte ou l'image
    for row in scopeDF.itertuples(index=False):
        x = row[1]
        y = row[2]
        rowType = row[3]
        rowValue = row[4]
        if(rowType=="Point"):
            pointCode += f"<div onclick=\"measure(this,'CH1')\" oncontextmenu=\"measure(this,'CH2')\" class=\"scope-dot\" id=\"dot{i}\" style=\"position: absolute;font-size: xx-large;color: {colors[3]};cursor: crosshair;top: {y - 15}px;left: {x - 4}px;line-height: 1;\">&#8226</div>\n"
            switchCode +=  f"case \"dot{i}\":\nfct = \"{rowValue}\";\nbreak;\n"
            i += 1
        elif(rowType=="Texte"):
            textCode +=  f"<div style=\"position: absolute;{textStyle}top: {y}px;left: {x}px;line-height: 1;\">{rowValue}</div>\n"
        elif(rowType=="Circuit"):
            circuitCode =  f"<div style=\"position: relative;width: {x}px;height: {y}px;\">\n<img src=\"{rowValue}\" alt=\"Circuit\" width=\"{x}\" height=\"{y}\">"
        elif(rowType=="Fonction"):
            helperCode +=  f"ggbelement.evalCommand("{rowValue}");\n"
            rowValue = rowValue.split("=")[0].strip()
            helperCode +=  f"ggbelement.setVisible("{rowValue}", false);\n"
        
    #Ouvre le gabarit et remplace les paramètres
    with open("gabaritScript.js", 'r') as baseScriptFile:
        baseScriptCode = baseScriptFile.read()
    
    baseScriptCode = baseScriptCode.replace("@@SWITCHCODE@@", switchCode)
    baseScriptCode = baseScriptCode.replace("@@HELPERCODE@@", helperCode)
    baseScriptCode = baseScriptCode.replace("@@SCALESCOPE@@", str(scale))
    baseScriptCode = baseScriptCode.replace("@@MATERIALID@@", applet)
    baseScriptCode = baseScriptCode.replace("@COLORNONE@", colors[3])
    baseScriptCode = baseScriptCode.replace("@COLORONE@", colors[0])
    baseScriptCode = baseScriptCode.replace("@COLORTWO@", colors[1]) 
    scriptCode = baseScriptCode.replace("@COLORBOTH@", colors[2])
    
    #Construit le code html de sortie
    htmlCode = circuitCode
    htmlCode += pointCode
    htmlCode += textCode
    htmlCode += "</div>"
    htmlCode += "<div id=\"ggbelement\"></div>"
    htmlCode += scriptCode
    
    return htmlCode


if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument("-o", "--output", help="Fichier de sortie dans lequel sera copier le code de l'oscilloscope virtuel", default="sortie.html")
    parser.add_argument("-s", "--scale", help="Facteur de mise à l'echelle de la fenetre de l'oscilloscope virtuel, une valeur de 1 donne une taille de 1350x800 px", default="1", type=float)
    parser.add_argument("-c", "--colors", nargs=4, help="Couleurs des points de tests, quatre valeurs doivent etre fournies soit en hexadecimal ou en utilisant les noms de couleurs HTML, l'ordre est canal 1, canal 2, canal 1 et 2, aucun canal. Ex: --colors Red Yellow Orange Blue", default=["Red", "Yellow", "Orange", "Blue"])
    parser.add_argument("-t", "--text" , help="Style CSS du texte ajoute sur l'image de circuit", default="font-size: medium;color: black;")
    parser.add_argument("-a", "--applet" , help="ID de l'appliquette GeoGebra", default="rphgwqbp")
    args = parser.parse_args()
    
    filepath = Path(args.input)
    
    if(filepath.suffix != ".xlsx" and filepath.suffix != ".xlsb"):
        print("ERREUR - Le fichier fourni n'est pas de type .xlsx ou .xlsb")
   
    htmlCode = generateScope(filepath, args.scale, args.colors, args.text, args.applet)

    outPath = Path(args.output)
        
    with open(outPath, 'w', encoding="UTF-8") as fileHTML:
        fileHTML.write(htmlCode)