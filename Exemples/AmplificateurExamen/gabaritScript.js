
<script src="https://www.geogebra.org/apps/deployggb.js"></script>
<script>
 
	var helperEvaluated = false;
	//Prepare les parametre de la fenetre
	var params = {
        "id": "ggbelement",
        "prerelease": false,
		//taille de la fenetre, ne pas changer car cela va rogner l'applet, ajuster le scale pour ajuster la taille
        "width": 1330,
        "height": 760,
        "showToolBar": false,
        "borderColor": null,
        "showMenuBar": false,
        "showAlgebraInput": false,
        "showResetIcon": false,
        "enableLabelDrags": false,
        "enableShiftDragZoom": false,
        "enableRightClick": false,
        "capturingThreshold": null,
        "showToolBarHelp": false,
        "errorDialogsActive": false,
        "useBrowserForJS": false,
        "enableRightClick": false,
        "enableLabelDrags": false,
		//ID de l'applet sur Geogebra
        'material_id': '@@MATERIALID@@',
		//Facteur de mise a l'echelle de la fenetre
        'scale': @@SCALESCOPE@@,
        "appletOnLoad": function(api) {},
    };

	//Charge l'applet dans le div "ggbelement" du code HTML
    var ggbApplet = new GGBApplet(params, false);
    window.addEventListener("load", function() {
        ggbApplet.inject('ggbelement');
    });

	// fonction appele lorsqu'un point de test est cliqué
    function measure(div, input) {
        var fct;
		//identifie la fonction a afficher en fonction du point de test cliqué
        switch (div.id) {
@@SWITCHCODE@@
            default:
                alert("Invalid measure");
        }
		//ajuste la couleur du point de test cliqué
        if (input == "CH1") {
            if (typeof measure.ch1 != 'undefined') {
                if (typeof measure.ch2 != 'undefined') {
                    if (measure.ch2.id == measure.ch1.id) {
                        measure.ch1.style.color = "@COLORTWO@";
                    } else {
                        measure.ch1.style.color = "@COLORNONE@";
                    }
                } else {
                    measure.ch1.style.color = "@COLORNONE@";
                }
            }
            div.style.color = "@COLORONE@";
            measure.ch1 = div;
            if (typeof measure.ch2 != 'undefined') {
                if (measure.ch2.id == measure.ch1.id) {
                    measure.ch1.style.color = "@COLORBOTH@";
                }
            }
        } else if (input == "CH2") {
            if (typeof measure.ch2 != 'undefined') {
                if (typeof measure.ch1 != 'undefined') {
                    if (measure.ch2.id == measure.ch1.id) {
                        measure.ch2.style.color = "@COLORONE@";
                    } else {
                        measure.ch2.style.color = "@COLORNONE@";
                    }
                } else {
                    measure.ch2.style.color = "@COLORNONE@";
                }
            }
            div.style.color = "@COLORTWO@";
            measure.ch2 = div;
            if (typeof measure.ch1 != 'undefined') {
                if (measure.ch2.id == measure.ch1.id) {
                    measure.ch2.style.color = "@COLORBOTH@";
                }
            }
        }
		
		if(!helperEvaluated)
		{
		@@HELPERCODE@@
		helperEvaluated=true;
		}
        var command = input + "input(x)=" + fct;
        ggbelement.evalCommand(command);
    }

    //Empêches le menu d'apparaitre quand on clique droit sur un point de test
    elements = document.getElementsByClassName("scope-dot")
    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener("contextmenu", (e) => {
            e.preventDefault()
        });
    }
</script>