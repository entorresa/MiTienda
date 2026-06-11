import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
import { ControlPanel } from "@web/search/control_panel/control_panel";  

class TarjetaSincronizacion extends Component {
    static components = { ControlPanel }; 
    static template = "api_mitienda_peru.TarjetaSincronizacion";
    setup(){
        this.orm = useService("orm");
        this.action = useService("action");
        

        this.state = useState({
            isFavorite: false,
            color: 0,
            sincronizaciones: [],
            chartData: {labels:[],data:[]},
            menuAbierto: false,
        });

        this.colors = [0,1,2,3,4,5,6,7,8,9,10,11];
        this.chartRef = useRef("chart");
        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            await this.cargarDatos();
            this.inicializarGrafica();
        });
    }

    async cargarDatos() {
        const syncData = await this.orm.call(
            'api_mitienda_peru.tablero',
            'get_sync_data',
            []
        );
        const sincs = await this.orm.call(
            'api_mitienda_peru.tablero',
            'get_ultimas_sincronizaciones',
            []
        );
        const prefs = await this.orm.call(
            'api_mitienda_peru.tablero',
            'get_preferencias',
            []
        );

        this.state.chartData = syncData;
        this.state.sincronizaciones = sincs;
        this.state.isFavorite = prefs.is_favorite;
        this.state.color = prefs.color;
    }

    inicializarGrafica(){
        const ctx = this.chartRef.el.getContext('2d');
        new Chart(ctx,{
            type: 'bar',
            data: {
                labels: this.state.chartData.labels,
                datasets: [{
                    label: 'Sincronizaciones',
                    data: this.state.chartData.data,
                    backgroundColor: '#7C7BAD',
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                plugins:{
                    legend:{display: false },
                    tooltip:{
                        enabled: true,
                        callback:{
                            label: function(context){
                                return ' ' + context.parsed.y + ' sincronizaciones';
                            } 
                        } 
                    }  
                }, 
                scales: {
                    y: {display: false,},
                    x: {grid:{display: false,}, ticks:{maxTicksLimit: 7}} 
                }
            }
        });
    }
/*
    configurarControlPanel(){
        this.controlPanel.update({
            title:{
                text: "Tablero de Sincronización",
            },
            favorite:{
                model: "api_mitienda_peru.tablero",
                label: "Vista actual",
                domain: [],
                context: { search_default_mis_favoritos: this.state.isFavorite },
                onAdd: (favorite) => {},   
            },
            filters:{
                mis_favoritos:{
                    label: "Mis favoritos",
                    domain: [["is_favorite","=",true]],
                    active: this.state.isFavorite,
                    onToggle: (active) =>{
                        this.state.isFavorite = active;
                        this.cargarDatos();
                    },
                }, 
            },
            search:{
                placeholder: "Buscar...",
                onSearch: (query) => {
                    console.log("Busqueda:",query);
                },
            },
        });
    } 
*/

    toggleMenu(){
        this.state.menuAbierto = !this.state.menuAbierto;
    }
    async toggleFavorite(){
        this.state.isFavorite = !this.state.isFavorite;
        await this.orm.call(
            'api_mitienda_peru.tablero',
            'set_favorite',
            [this.state.isFavorite]
        );
        await this.cargarDatos();
        this.configurarControlPanel();
    }
    async setColor(color){
        this.state.color = color;
        this.state.menuAbierto = false;
        await this.orm.call(
            'api_mitienda_peru.tablero',
            'set_color',
            [color]
        );
    }
    verVenta(saleOrderId){
        if(!saleOrderId) return;
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            res_id: saleOrderId,
            views:[[false,'form']],
        });
    }
    verMas(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'mitienda.pe.sale.order',
            views:[[false,'list']],
        });
    }
}
registry.category("actions").add(
    "api_mitienda_peru.tablero_sincronizacion",
    TarjetaSincronizacion
);

