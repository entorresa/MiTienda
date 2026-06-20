// /** @odoo-module **/
// import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
// import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
// import { ControlPanel } from "@web/search/control_panel/control_panel";  

const CHARTJS = "/web/static/lib/Chart/Chart.js";
async function ensureChartJsLoaded(){
    if(window.Chart)
        return;
    await loadJS(CHARTJS);
}

function renderChart(canvas){
    if(canvas.dataset.chartRendered === "1")
        return;
    const raw = canvas.getAttribute("data-chart");
    if(!raw)
        return;
    let parsed;
    try{
        parsed = JSON.parse(raw);
    } catch(e){
        console.warn("[mitienda] No se pudo parsear data-chart",e);
        return;
    }
    const labels = parsed.labels || [];
    const data = parsed.data || [];
    
    new window.Chart(canvas, {
        type:"bar",
        data:{
            labels,
            datasets:[
                {
                    label:"Sincronizaciones",
                    data,
                    backgroundColor: "#714B67",
                    borderRadius: 4,
                    maxBarThickness: 28,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
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
            },
            scales:{
                y:{
                    beginAtZero: true,
                    display: false,
                },
            },
        },
    });
    canvas.dataset.chartRendered = "1";
}

function scanAndRender(){
    const canvases = document.querySelectorAll(".o_mitienda_sync_chart");
    canvases.forEach(renderChart);
}

registry.category("services").add("mitienda_sync_chart_service",{
    async start(){
        await ensureChartJsLoaded();
        scanAndRender();
        const observer = new MutationObserver(()=>{
            scanAndRender();
        });
        observer.observe(document.body,{childList: true, subtree:true});
    },
});


registry.category("services").add("mitienda_pv_click_handler",{
    start(env){
        document.addEventListener("click", (ev) => {
            const link = ev.target.closest(".o_siat_pv_name");
            if(!link)
                return;
            ev.preventDefault();
            ev.stopPropagation();
            const saleId = link.dataset.saleId;
            const pvId = link.dataset.pvId;

            if(saleId){
                env.services.action.doAction({
                    type:"ir.actions.act_window",
                    res_model:"sale.order",
                    res_id:parseInt(saleId,10),
                    views:[[false,"form"]],
                    target:"current",
                });
            } else if (pvId){
                env.services.action.doAction({
                    type:"ir.actions.act_window",
                    res_model:"siat.punto.venta",
                    res_id: parseInt(pvId,10),
                    views:[[false,"form"]],
                    target:"current",
                });
            }
            
        });
  },
});


// class TarjetaSincronizacion extends Component {
//     static components = { ControlPanel }; 
//     static template = "api_mitienda_peru.TarjetaSincronizacion";
//     setup(){
//         this.orm = useService("orm");
//         this.action = useService("action");
        

//         this.state = useState({
//             isFavorite: false,
//             color: 0,
//             sincronizaciones: [],
//             chartData: {labels:[],data:[]},
//             menuAbierto: false,
//         });

//         this.colors = [0,1,2,3,4,5,6,7,8,9,10,11];
//         this.chartRef = useRef("chart");
//         onMounted(async () => {
//             await loadJS("/web/static/lib/Chart/Chart.js");
//             await this.cargarDatos();
//             this.inicializarGrafica();
//         });
//     }

//     async cargarDatos() {
//         const syncData = await this.orm.call(
//             'mitienda.pe.tablero',
//             'get_sync_data',
//             []
//         );
//         const sincs = await this.orm.call(
//             'mitienda.pe.tablero',
//             'get_ultimas_sincronizaciones',
//             []
//         );
//         const prefs = await this.orm.call(
//             'mitienda.pe.tablero',
//             'get_preferencias',
//             []
//         );

//         this.state.chartData = syncData;
//         this.state.sincronizaciones = sincs;
//         this.state.isFavorite = prefs.is_favorite;
//         this.state.color = prefs.color;
//     }

//     inicializarGrafica(){
//         const ctx = this.chartRef.el.getContext('2d');
//         new Chart(ctx,{
//             type: 'bar',
//             data: {
//                 labels: this.state.chartData.labels,
//                 datasets: [{
//                     label: 'Sincronizaciones',
//                     data: this.state.chartData.data,
//                     backgroundColor: '#7C7BAD',
//                     borderRadius: 4,
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 plugins:{
//                     legend:{display: false },
//                     tooltip:{
//                         enabled: true,
//                         callback:{
//                             label: function(context){
//                                 return ' ' + context.parsed.y + ' sincronizaciones';
//                             } 
//                         } 
//                     }  
//                 }, 
//                 scales: {
//                     y: {display: false,},
//                     x: {grid:{display: false,}, ticks:{maxTicksLimit: 7}} 
//                 }
//             }
//         });
//     }

//     toggleMenu(){
//         this.state.menuAbierto = !this.state.menuAbierto;
//     }
//     async toggleFavorite(){
//         this.state.isFavorite = !this.state.isFavorite;
//         await this.orm.call(
//             'mitienda.pe.tablero',
//             'set_favorite',
//             [this.state.isFavorite]
//         );
//         await this.cargarDatos();
//         this.configurarControlPanel();
//     }
//     async setColor(color){
//         this.state.color = color;
//         this.state.menuAbierto = false;
//         await this.orm.call(
//             'mitienda.pe.tablero',
//             'set_color',
//             [color]
//         );
//     }
//     verVenta(saleOrderId){
//         if(!saleOrderId) return;
//         this.action.doAction({
//             type: 'ir.actions.act_window',
//             res_model: 'sale.order',
//             res_id: saleOrderId,
//             views:[[false,'form']],
//         });
//     }
//     verMas(){
//         this.action.doAction({
//             type: 'ir.actions.act_window',
//             res_model: 'mitienda.pe.sale.order',
//             views:[[false,'list']],
//         });
//     }
// }
// registry.category("actions").add(
//     "mitienda_pe_tablero_view",
//     TarjetaSincronizacion
// );

