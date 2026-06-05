/**
 * expose common functions for other JS libraries to import
 *  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export
 */

function export_test(){
    console.log("export test");
}

/**
 * Return the big array of element IDs that make up the compass
 */
function getElems(){
    console.log("in shared function");
    let elems = [
        'q-1',
        's1-t',
        's1-1', 's1-2', 's1-3', 's1-4', 's1-5', 's1-6',
        's2-t',
        's2-1', 's2-2', 's2-3', 's2-4', 's2-5', 's2-6',
        's3-t',
        's3-1', 's3-2', 's3-3', 's3-4', 's3-5', 's3-6',
        's4-t',
        's4-1', 's4-2', 's4-3', 's4-4', 's4-5', 's4-6',
        's5-t',
        's5-1', 's5-2', 's5-3', 's5-4', 's5-5', 's5-6',
        'q-2',
        's6-t',
        's6-1', 's6-2', 's6-3', 's6-4', 's6-5', 's6-6',
        's7-t',
        's7-1', 's7-2', 's7-3', 's7-4', 's7-5', 's7-6',
        's8-t',
        's8-1', 's8-2', 's8-3', 's8-4', 's8-5', 's8-6',
        's9-t',
        's9-1', 's9-2', 's9-3', 's9-4', 's9-5', 's9-6',
        'q-3',
        's10-t',
        's10-1', 's10-2', 's10-3', 's10-4', 's10-5', 's10-6',
        's11-t',
        's11-1', 's11-2', 's11-3', 's11-4', 's11-5', 's11-6',
        's12-t',
        's12-1', 's12-2', 's12-3', 's12-4', 's12-5', 's12-6',
        's13-t',
        's13-1', 's13-2', 's13-3', 's13-4', 's13-5', 's13-6',
        'q-4',
        's14-t',
        's14-1', 's14-2', 's14-3', 's14-4', 's14-5', 's14-6',
        's15-t',
        's15-1', 's15-2', 's15-3', 's15-4', 's15-5', 's15-6',
        's16-t',
        's16-1', 's16-2', 's16-3', 's16-4', 's16-5', 's16-6',
        's17-t',
        's17-1', 's17-2', 's17-3', 's17-4', 's17-5', 's17-6'
    ];

    return elems;
}
