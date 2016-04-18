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
             * Here we manually set orbiting object ids and then call
             * a cgi script to get the orbits.
             */
            if(typeof RENDER_LIST !== "undefined"){       

                var getOrbitsHandler = function(response){

                    console.log(response.sup);
                };

                var url = "/mpc/service/get-orbits.cgi";
                var arg = "objectIds="+ RENDER_LIST.join(",");
                Utils.ajax(url, arg, getOrbitsHandler);
            }
        }    
    };
})(this);