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
             */
            if(typeof RENDER_LIST !== "undefined"){       

                var getOrbitsHandler = function(response){
                    
                    if(response.success) this.solSys.drawOrbits(response.data);
                };

                var url = "/mpc/service/api/get-orbits.cgi";
                var arg = "ids="+ RENDER_LIST.join(",");
                Utils.ajax(url, arg, getOrbitsHandler.bind(this));
            }
        }    
    };
})(this);