$(document).ready(function () {
    $("#id_name").jqxTooltip({
        content: '<i>Name for this LogDef</i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });

    $("#id_desc").jqxTooltip({
        content: '<i>Description of the Log Attrivute</i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });

    $("#id_is_qual_data").jqxTooltip({
        content:'<i>If there is quantatative(non-numeric) check the box, otherwise leave unchcked <br/></i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_units").jqxTooltip({
        content: "<i> Units of the quantatative value</i>",
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_low_low").jqxTooltip({
        content: '<i>Absolute lower bound, values cannot be below this value</i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_high_high").jqxTooltip({
        content: '<i>Absolute upper bound, values cannot be above this value </i>',
        position: 'mouse',
        name: 'movieTooltip'
    });
    $("#id_low").jqxTooltip({
        content: '<i>Soft lower bound, values below this will trigger a flag </i>',
        position: 'mouse',
        name: 'phaseTooltip'
    });
    $("#id_high").jqxTooltip({
        content: '<i>Soft upper bound, values above this will trigger a flag </i>',
        position: 'mouse',
        name: 'movieTooltip'
    });
    $("#id_high").jqxTooltip({
        content: '<i>Soft upper bound, values above this will trigger a flag </i>',
        position: 'mouse',
        name: 'movieTooltip'
    });
    $("#submit").jqxTooltip({
        content: '<i>Create this Log Attribute</i>',
        position: 'mouse',
        name: 'movieTooltip'
    });
    $("#done").jqxTooltip({
        content: '<i>Finished, does not save this Log Attribute</i>',
        position: 'mouse',
        name: 'movieTooltip'
    });
});
