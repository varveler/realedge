import React from 'react'
import Button from '@material-ui/core/Button' 
import {takeScreenshot} from "electron-screencapture";
 





class ScanButton extends React.Component{
     
    

    startScan = () => {
        takeScreenshot({x: 0, y: 0, width: 800, height: 600}).then(result => {
            console.log(result);
        });     
        
        
    }

    render(){
        return(
            <Button variant="contained" color="primary" onClick={()=>this.startScan()}>
                Scan
            </Button>
        )
    }
}

export default ScanButton;