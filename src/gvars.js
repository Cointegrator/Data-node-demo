// response code:
// 100: normal
// 200: no session
// 201: system error
// import {isRelease} from "../../config.json"

export const gvars = {
    isRelease: 0,
    num_default_steps_to_show: 15000000,// the number of days to be shown by default, a very very large value means showing all
    num_latest_steps_to_show: 150,      // the numbber of latest days to be shown
    trans: {},						    // the global transformation matrix for linePlot and stackPlot

    project_length_default: 1,          // the default projection length, will never change
    shape_length_default: 10,           // the default shape length, will never change
    project_margin_default: 50,         // the default projection margin,, matches within this margin will be ignored

    show_node_when_lessthan: 100,       // show step markers
    circleMarkerRadius: 5,              // size of the circle marker when zoom in
    
    x_margin_ratio: 0.001,
    y_margin_ratio: 0.001,
    projection_x_margin_ratio: 0.05,
    projection_y_margin_ratio: 0.15,

    field_of_invalid_date: "invalid_date",

    month: ['Jan','Feb','Mar','Apr','May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec'],

    // matched curve color (the vertical line and rectange for matched region)
    match_clr: ['#ff7f0e', 	
        '#1f77b4', '#2ca02c', '#d62728', 
        '#9467bd', '#8c564b', '#e377c2', 
        '#7f7f7f', '#bcbd22', '#17becf'
    ],
    // the curves in the line chart
    curve_clr: ["gray", "orange"],
    curve_clr1: ["rgb(236,191,110)", "rgb(88,57,217)"],
    // the stacked area chart color
    area_clr: ['#ff7f0e', 	
        '#1f77b4', '#2ca02c', '#d62728', 
        '#9467bd', '#8c564b', '#e377c2', 
        '#7f7f7f', '#bcbd22', '#17becf'],

    color_red: "rgb(246, 192, 198)",    //slightly "red"
    color_green: "rgb(199, 241, 215)",  //slightly "green" 
    color_gray: "rgb(240,240,240)",     // slightly "gray"

    ohlcv_default: 'Close',

    colorHistory: "rgba(235, 191, 110, 0.2)",
    colorFuture: "rgba(86, 58, 219, 0.1)",

    colorBgHistory: "rgba(235, 191, 110, 0.0)", // the left rectangle
    colorBgFuture: "rgba(86, 58, 219, 0.1)",    // the right rectangle
    colorProjStd: "rgb(79, 110, 216)",
    alphaProjStd: 0.1,
    colorProjMean: "rgb(80,111,216)",

    text_disclaimer: '<p style="text-align:left">Trading leveraged products carries a high degree of risk and you could lose more than your initial deposit. Any future projections, data points, opinions, chats, messages, news, research, analyses, prices, or other information contained on the IndicatorLab website are provided as general market information for educational and entertainment purposes only and do not constitute investment advice. The Website should not be relied upon as a substitute for extensive independent market research before making your actual trading decisions. Projections, data points, opinions, market data, recommendations, or any other content is subject to change at any time without notice. IndicatorLab will not accept liability for any loss or damage, including without limitation any loss of profit, which may arise directly or indirectly from the use of or reliance on such information.</p>' +
    '<p style="text-align:left">You should always understand that PAST PERFORMANCE IS NOT NECESSARILY INDICATIVE OF FUTURE RESULTS. Future projections (trend and consistency) have many inherent limitations, some of which are mentioned below. No representation is made that any account will or is likely to achieve profits or losses similar to the projected future trend regardless of the confidence value. There are frequently marked differences between projected trends and actual results subsequently achieved by any particular trading program.</p>' +
    '<p style="text-align:left">Decisions to buy, sell, hold or trade in securities, commodities and other investments involve risk and are best made based on the advice of qualified financial professionals. Any trading in securities or other investments involves a risk of substantial losses. Please understand that trading is a very difficult career. By using IndicatorLab service, you are not guaranteed future success. Under no circumstances shall we be liable for any loss or damage you or anyone else incurs as a result of any trading or investment activity that you or anyone else engages in based on any information or material you receive through IndicatorLab or our services. You agree not to hold IndicatorLab or any Admins liable for any possible claim for damages arising from any decision you make based on the content or other information made available to you through the Service.</p>' +
    '<p style="text-align:left">IndicatorLab cannot and does not represent or guarantee that any of the information (e.g., indicators, history price of an asset, dates) available through our services or on IndicatorLab is accurate, reliable, current, complete, or appropriate for your needs. We do not control and are not responsible for what other users post on the IndicatorLab services (e.g., discord, Twitter, YouTube, etc). </p>',

    test_user_group_name: 'alpha_pioneer', // will be used if Register.vue isRquireRegCode is true

    default_point: 100,                 // default point for a newly registered user
    default_point_ap: 200,              // default point for AP users

    maxStockCurvePointForSampling: 500,        // large that this number will trigger the data subsampling

    default_time_scale_options: [
        {value: '1d', label: '1 day'},
        {value: '1h', label: '1 hour'},
    ],

    field_of_non_data: "invalid_date", // this is defined from the python side

    newsTimeScaleUTC: true, // the news view uses UTC time scale or not
}