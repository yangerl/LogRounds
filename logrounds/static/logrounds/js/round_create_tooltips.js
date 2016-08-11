$(document).ready(function () {
    $("#id_rt_name").jqxTooltip({
        content: '<i>Name for this RoundType</i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_period").jqxTooltip({
        content: '<i>Periodicity of the log. Time between Log Entries</i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_rt_desc").jqxTooltip({
        content: '<i>Description of the log</i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_start_date").jqxTooltip({
        content: 
                "<i>Start date of the log before 'phase'-ing. \
                If there is no phase the log starts at midnight on the date.\
                Otherwise, the first required entry will be the phase+start_date. </i>",
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_phase_days").jqxTooltip({
        content: '<i>Offsets the start date by entered number of days</i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_phase_hours").jqxTooltip({
        content: '<i>Offsets the start date by entered number of hours</i>',
        position: 'mouse',
        name: 'movieTooltip'
    });
    $("#id_phase_min").jqxTooltip({
        content: '<i>Offsets the start date by entered number of minutes</i>',
        position: 'mouse',
        name: 'movieTooltip'
    });
});
