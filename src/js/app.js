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
            var RENDER_LIST = [

                "EM_Bary"
            ];

            if(typeof RENDER_LIST !== "undefined"){       

                var getOrbitsHandler = function(response){
                    
                    if(response.success) this.solSys.drawVectorOrbits(response.data);
                };

                var url = "/mpc/service/api/get-orbits.cgi";
                var arg = "ids="+ RENDER_LIST.join(",") + "&db=12";
                Utils.ajax(url, arg, getOrbitsHandler.bind(this));
            }
        }    
    };
})(this);