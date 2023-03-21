	<?php 
	header('Content-Type: application/json; charset=utf-8');
	// echo file_get_contents('php://input');
	if(file_get_contents('php://input') != null){
	   // $_POST = json_decode(file_get_contents('php://input'), true);
	   echo file_get_contents('php://input');  //this is an object
	   // echo json_encode(file_get_contents('php://input'),true) . "\n";
	   // echo json_decode(file_get_contents('php://input'),true);
	}
	else{
	    echo json_encode(array('status'=>'ok','message'=>'retrieve data from current'),true);
	}
	

	?>

