function arrayRemoveItem (arr, item){
	for(var i = arr.length-1; i >= 0; i--){
	    if(arr[i] == item){
	        return arr.splice(i,1);
	    }
	}
}