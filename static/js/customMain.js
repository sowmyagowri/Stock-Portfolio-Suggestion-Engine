jQuery(function(){

    /**
     * Declaring variables 
     */

    var temp, j , i, obj , flag = false;

    /**
     * Form validation and checking
     * @param  {[type]} e){                             flag [description]
     * @return {[type]}      [description]
     */

    jQuery('.compute-report').on('submit',function(e){

        flag = false;

        // Count how many checkboxes are ticked;
        i = 0;
        jQuery('.compute-report input[type="checkbox"]').each(function(){

             if( jQuery(this).is(':checked') )
                i++;

        });

        if(i > 2) {
             temp = 'Only 2 Investing options are permitted !';
             flag = true;   
        }

        if(i === 0) {
             temp = 'Please select atleast one investing option !';
             flag = true;   
        }

       if(flag === true) {
            alert(temp);

            return false; 
       }
    })
});