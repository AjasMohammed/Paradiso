import * as React from "react";
import "./Stepper.css";
import Box from "@mui/material/Box";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepButton from "@mui/material/StepButton";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import CheckoutForm from "../CheckoutForm/CheckoutForm";
import StripeElement from "../StripeElement/StripeElement";

const steps = ["Enter User Details", "Enter Payment Details", "Order Details"];

const checkoutComponents = [<CheckoutForm />, <StripeElement />];

export default function HorizontalNonLinearStepper() {
  const [activeStep, setActiveStep] = React.useState(0);
  const [completed, setCompleted] = React.useState({});

  // const [userDetails, setUserDetails] = React.useState({
  //   // Define initial user details
  //   // Example: name: "", email: ""
  // });
  // const [paymentDetails, setPaymentDetails] = React.useState({});

  const totalSteps = () => {
    return steps.length;
  };

  const completedSteps = () => {
    return Object.keys(completed).length;
  };

  const isLastStep = () => {
    return activeStep === totalSteps() - 1;
  };

  const allStepsCompleted = () => {
    return completedSteps() === totalSteps();
  };

  const handleNext = () => {
    const newActiveStep =
      isLastStep() && !allStepsCompleted()
        ? // It's the last step, but not all steps have been completed,
          // find the first step that has been completed
          steps.findIndex((step, i) => !(i in completed))
        : activeStep + 1;
    setActiveStep(newActiveStep);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
    const newCompleted = completed;
    console.log(activeStep);
    newCompleted[activeStep - 1] = false;
    setCompleted(newCompleted);
  };

  const handleStep = (step) => () => {
    setActiveStep(step);
  };

  const handleComplete = () => {
    const newCompleted = completed;
    newCompleted[activeStep] = true;
    setCompleted(newCompleted);
    handleNext();
  };

  const handleReset = () => {
    setActiveStep(0);
    setCompleted({});
  };

  // const handleUserDetails = (details) => {
  //   setUserDetails(details);

  //   handleComplete();
  // };

  // // Callback function to receive payment details from StripeElement
  // const handlePaymentDetails = (details) => {
  //   setPaymentDetails(details);
  //   // axios.post("shop/place-order/", details);
  //   handleComplete();
  // };

  return (
    <Box sx={{ width: "100%" }}>
      <Stepper nonLinear activeStep={activeStep} alternativeLabel>
        {steps.map((label, index) => (
          <Step key={label} completed={completed[index]}>
            <StepButton onClick={handleStep(index)} disabled="true">
              {label}
            </StepButton>
          </Step>
        ))}
      </Stepper>
      <div id="stepper">
        {allStepsCompleted() ? (
          <React.Fragment>
            <Typography sx={{ mt: 2, mb: 1 }}>
              All steps completed - you&apos;re finished
            </Typography>
            <Box sx={{ display: "flex", flexDirection: "row", pt: 2 }}>
              <Box sx={{ flex: "1 1 auto" }} />
              <Button onClick={handleReset}>Reset</Button>
            </Box>
          </React.Fragment>
        ) : (
          <React.Fragment>
            <div className="checkout-components">
              {activeStep === 0 && (
                <CheckoutForm onUserDetails={handleComplete} />
              )}
              {activeStep === 1 && (
                <StripeElement onPaymentDetails={handleComplete} />
              )}
            </div>
            <Box sx={{ display: "flex", flexDirection: "row", pt: 2 }}>
              <Button
                className="btn"
                disabled={activeStep === 0}
                onClick={handleBack}
                sx={{ mr: 1, color: "#000" }}
              >
                Back
              </Button>
              {/* <Box sx={{ flex: "1 1 auto" }} />
              <Button onClick={handleNext} sx={{ mr: 1 }}>
                Next
              </Button>
              {activeStep !== steps.length &&
                (completed[activeStep] ? (
                  <Typography
                    variant="caption"
                    sx={{ display: "inline-block" }}
                  >
                    Step {activeStep + 1} already completed
                  </Typography>
                ) : (
                  <Button onClick={handleComplete}>
                    {completedSteps() === totalSteps() - 1
                      ? "Finish"
                      : "Complete Step"}
                  </Button>
                ))} */}
            </Box>
          </React.Fragment>
        )}
      </div>
    </Box>
  );
}
