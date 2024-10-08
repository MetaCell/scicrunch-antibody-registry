import React from "react";
import { FieldConfig } from "formik";
import {
  Box,
  Card,
  CardActionArea,
  CardContent,
  Typography,
  Stack,
  Link,
  Radio,
} from "@mui/material";
import { useTheme } from "@mui/system";
import {
  CompanyIcon,
  UserWithBackgroundIcon,
  HorizontalThreeDotsIcon,
} from "../icons";
import StepNavigation from "./StepNavigation";

interface AbTypeStepProps extends FieldConfig {
  label: string;
  selectedValue: string;
  handleChange: (type: string) => void;
  next: () => {};
  previous: () => {};
  hasPrevious: boolean;
}

const TypeChoiceCard = ({ label, icon, handleClick, selectedValue, type }) => {
  const classes = {
    card: {
      flexGrow: 1,
      maxWidth: 232,
      border: selectedValue === type ? "2px solid" : "1px solid",
      borderColor: selectedValue === type ? "primary.main" : "grey.200",
      backgroundColor: selectedValue === type ? "#F9FCFE" : null,
    },
    cardLabel: {
      color: "grey.700",
    },
  };

  return (
    (<Card elevation={0} sx={classes.card}>
      <CardActionArea onClick={handleClick}>
        <CardContent sx={{ py: 3, px: 2 }}>
          <Stack
            spacing={2}
            sx={{
              display: "flex",
              alignItems: "center"
            }}>
            {icon}
            <Typography
              gutterBottom
              variant="subtitle2"
              component="div"
              sx={classes.cardLabel}
            >
              {label}
            </Typography>
            <Radio checked={selectedValue === type} size="small" />
          </Stack>
        </CardContent>
      </CardActionArea>
    </Card>)
  );
};

const styles = {
  title: {
    paddingTop: 15,
    paddingBottom: 5,
  },
  content: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap",
  },
};

const AbTypeStep = ({ label, ...props }: AbTypeStepProps) => {
  

  return (
    <>
      <Box className="antibody-type-choose">
        <Typography sx={styles.title} variant="h1">
          1. Type of antibody
        </Typography>
        <Stack direction="row" spacing={1.5} sx={styles.content}>
          <TypeChoiceCard
            label="Commercial Antibody/Kit"
            icon={<CompanyIcon />}
            handleClick={() => props.handleChange("commercial")}
            selectedValue={props.selectedValue}
            type="commercial"
          />
          <TypeChoiceCard
            label="Personal Antibody"
            icon={<UserWithBackgroundIcon />}
            handleClick={() => props.handleChange("personal")}
            selectedValue={props.selectedValue}
            type="personal"
          />
          <TypeChoiceCard
            label="Other/Custom Antibody"
            icon={<HorizontalThreeDotsIcon />}
            handleClick={() => props.handleChange("other")}
            selectedValue={props.selectedValue}
            type="other"
          />
        </Stack>
        <Typography variant="subtitle2" sx={{ color: "grey.500", mt: 5 }}>
          Want to do a bulk upload? <Link className="link-contact" href="mailto:abr-help@scicrunch.org">Contact us</Link>
        </Typography>
      </Box>
      <StepNavigation
        previous={props.previous}
        next={props.next}
        hasPrevious={props.hasPrevious}
        activeStep={1}
      />
    </>
  );
};

export default AbTypeStep;
