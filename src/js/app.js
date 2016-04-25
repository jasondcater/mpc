(function(global){

    "use strict";

    /**
     * main application controller,
     * builds the widgets,
     * handles the inter-widget eventing,
     * sets and gets global variables,
     * catches and routes global ajax responses
     */

    global.App = {

        initialize : function(){

            this.solSys = new SolSys();
            
            /**
             * Here we manually set orbiting object ids on RENDER_LIST
             * and then call a cgi script to get the orbits.
             * 
             * Also the data is being pulled from a Redis database. Different
             * orbit types are kept in different databases we must specify
             * the proper DB number. They are as follows.
             * 
             *  http://minorplanetcenter.net/blog/asteroid-classification-i-dynamics/ 
             *  1 = Amor
             *  12 = Planets
             */

//STANDARD ORBITAL ELEMS
            var RENDER_LIST = [

                "Mercury",
                "Venus",
                "EM_Bary",
                "Mars",
                "Jupiter",
                "Saturn",
                "Uranus",
                "Neptune",
                "Pluto"
            ];

            var vectorOrbitHandler = function(response){

                if(response.success) this.solSys.drawVectorOrbits(response.data);
            }

            var url = "/mpc/service/api/get-vector-orbits.cgi";
            var arg = "ids="+ RENDER_LIST.join(",") + "&db=12";
            Utils.ajax(url, arg, vectorOrbitHandler.bind(this));

//KELPER ORBITAL ELEMS TO X,Y,Z
            //args for pluto orbit
            var semiMaj = 39.48211675;
            var dateOfPeriapsis = "03/01/2016 12:00:00";
            var eccentricity = 0.24882730;
            var orbitTime = 90581 * 24 * 60 * 60
            var inclination = 17.14001206 ;
            var longitudeOfPeriapsis = 224.06891629
            var ascNode = 110.30393684;
            var argOfPeriapsis = longitudeOfPeriapsis-ascNode;

            var keplerOrbitHandler = function(response){

                if(response.success) this.solSys.drawPointOrbits(response.data);
            }

            var url = "/mpc/service/api/gen-xyz-frm-kep.cgi";
            var arg = "a="+ semiMaj +"&p="+ dateOfPeriapsis +"&o="+ orbitTime +"&e="+ eccentricity 
                +"&i="+ inclination +"&w="+ argOfPeriapsis +"&r="+ ascNode;
            Utils.ajax(url, arg, keplerOrbitHandler.bind(this));

            this.solSys.drawSpecialOrbit(pluto)

//STRAIGHT X,Y,Z  EPHEMERIDES
            var pointOrbitHandler = function(response){

                if(response.success) this.solSys.drawPointOrbits(response.data);
            }

            var url = "/mpc/service/api/get-point-orbits.cgi";
            var arg = "";
            //Utils.ajax(url, arg, pointOrbitHandler.bind(this));
        }
    };
})(this);