import React from "react";
import {useNavigate} from "react-router-dom";
import { Nav, NavLink, NavMenu }
	from "./NavbarElements";

const Navbar = () => {
    const navigate = useNavigate();
    var stepsList = ["step1Div", "step2Div", "step3Div", "step4Div", "step5Div", "step6Div"]
    var trainingSteps = 4

    const onClickStep1 = () => {
        // console.log("hello")
        
        for (let index = 0; index < stepsList.length; index += 1) {
            if (index != 0) {
                var stepElement = document.getElementById(stepsList[index]);
                stepElement.classList.add("stepDivBackground");
                stepElement.classList.remove("onclickColor");
            }
        }
        var step1Element = document.getElementById("step1Div");
        step1Element.classList.remove("stepDivBackground");
        step1Element.classList.add("onclickColor");
        var phaseElement = document.getElementById("trainingText");
        phaseElement.classList.add("onclickTextColor")
        var phaseElement = document.getElementById("testingText");
        phaseElement.classList.remove("onclickTextColor")
        navigate('/step1');

    }
    const onClickStep2 = () => {
        // console.log("hello")
        for (let index = 0; index < stepsList.length; index += 1) {
            if (index != 1) {
                var stepElement = document.getElementById(stepsList[index]);
                stepElement.classList.add("stepDivBackground");
                stepElement.classList.remove("onclickColor");
            }
        }
        var step2Element = document.getElementById("step2Div");
        step2Element.classList.remove("stepDivBackground");
        step2Element.classList.add("onclickColor");
        var phaseElement = document.getElementById("trainingText");
        phaseElement.classList.add("onclickTextColor")
        var phaseElement = document.getElementById("testingText");
        phaseElement.classList.remove("onclickTextColor")
        navigate('/step2');
    }
    const onClickStep3 = () => {
        // console.log("hello")
        for (let index = 0; index < stepsList.length; index += 1) {
            if (index != 2) {
                var stepElement = document.getElementById(stepsList[index]);
                stepElement.classList.add("stepDivBackground");
                stepElement.classList.remove("onclickColor");
            }
        }
        var step3Element = document.getElementById("step3Div");
        step3Element.classList.remove("stepDivBackground");
        step3Element.classList.add("onclickColor");
        var phaseElement = document.getElementById("trainingText");
        phaseElement.classList.add("onclickTextColor")
        var phaseElement = document.getElementById("testingText");
        phaseElement.classList.remove("onclickTextColor")
        navigate('/step3');
    }
    const onClickStep4 = () => {
        // console.log("hello")
        for (let index = 0; index < stepsList.length; index += 1) {
            if (index != 3) {
                var stepElement = document.getElementById(stepsList[index]);
                stepElement.classList.add("stepDivBackground");
                stepElement.classList.remove("onclickColor");
            }
        }
        var step4Element = document.getElementById("step4Div");
        step4Element.classList.remove("stepDivBackground");
        step4Element.classList.add("onclickColor");
        var phaseElement = document.getElementById("trainingText");
        phaseElement.classList.add("onclickTextColor")
        var phaseElement = document.getElementById("testingText");
        phaseElement.classList.remove("onclickTextColor")
        navigate('/step4');
    }
    const onClickStep5 = () => {
        // console.log("hello")
        for (let index = 0; index < stepsList.length; index += 1) {
            if (index != 4) {
                var stepElement = document.getElementById(stepsList[index]);
                stepElement.classList.add("stepDivBackground");
                stepElement.classList.remove("onclickColor");
            }
        }
        var step5Element = document.getElementById("step5Div");
        step5Element.classList.remove("stepDivBackground");
        step5Element.classList.add("onclickColor");
        var phaseElement = document.getElementById("testingText");
        phaseElement.classList.add("onclickTextColor")
        var phaseElement = document.getElementById("trainingText");
        phaseElement.classList.remove("onclickTextColor")
        navigate('/step5');
    }
    const onClickStep6 = () => {
        // console.log("hello")
        for (let index = 0; index < stepsList.length; index += 1) {
            if (index != 5) {
                var stepElement = document.getElementById(stepsList[index]);
                stepElement.classList.add("stepDivBackground");
                stepElement.classList.remove("onclickColor");
            }
        }
        var step6Element = document.getElementById("step6Div");
        step6Element.classList.remove("stepDivBackground");
        step6Element.classList.add("onclickColor");
        var phaseElement = document.getElementById("testingText");
        phaseElement.classList.add("onclickTextColor")
        var phaseElement = document.getElementById("trainingText");
        phaseElement.classList.remove("onclickTextColor")
        navigate('/step6');
    }
	return (
		<>
            {/* <div class="phases">
                <div class="training">
                    Training phase
                </div>
                {/* <div class="testing">
                    Testing phase
                </div> */}
            {/* </div> */}
            <div class="navContainer">
				<div class="navBar">
                    {/* <div class="trainingPhase"> */}
                        <div class="phasesBlock">
                            <div id="trainingText">
                                    Training Phase
                            </div>
                        </div>
                        <div class="phasesBlock">
                            <div>
                                
                            </div>
                        </div>
                        <div class="phasesBlock">
                            <div >
                               
                            </div>
                        </div>
                        <div class="phasesBlock">
                            <div >
                               
                            </div>
                        </div>
                    {/* </div> */}
                    {/* <div class="testingPhase"> */}
                       <div class="phasesBlock">
                            <div id="testingText">
                                Testing Phase
                            </div>
                        </div>
                        <div class="phasesBlock">
                            <div >
            
                            </div>
                        </div> 
                    {/* </div> */}
                    
				</div>
			</div>
			<div class="navContainer">
				<div class="navBar">
                    {/* <div class="trainingPhase"> */}
                        <div class="stepBlock" id="step1Div" onClick={onClickStep1}>
                            <div to="/step1" >
                                    Step 1
                            </div>
                        </div>
                        <div class="stepBlock" id="step2Div" onClick={onClickStep2}>
                            <div to="/step2" activeStyle>
                                Step 2
                            </div>
                        </div>
                        <div class="stepBlock" id="step3Div" onClick={onClickStep3}>
                            <div to="/step3" activeStyle>
                                Step 3
                            </div>
                        </div>
                        <div class="stepBlock" id="step4Div" onClick={onClickStep4}>
                            <div to="/step4" activeStyle>
                                Step 4
                            </div>
                        </div>
                    {/* </div> */}
                    {/* <div class="testingPhase"> */}
                       <div class="stepBlock" id="step5Div" onClick={onClickStep5}>
                            <div to="/step5" activeStyle>
                                Step 5
                            </div>
                        </div>
                        <div class="stepBlock" id="step6Div" onClick={onClickStep6}>
                            <div to="/step6" activeStyle>
                                Step 6
                            </div>
                        </div> 
                    {/* </div> */}
                    
				</div>
			</div>
		</>
	);
};

export default Navbar;
