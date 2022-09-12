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

interface AbTypeStep extends FieldConfig {
  label: string;
  selectedValue: string;
  handleChange: (type: string) => void;
}

const TypeChoiceCard = ({ children, label, icon, handleClick }) => {
  const classes = {
    card: {
      flexGrow: 1,
      maxWidth: 232,
      border: "1px solid",
      borderColor: "grey.200",
    },
    cardLabel: {
      color: "grey.700",
    },
  };
  return (
    <Card elevation={0} sx={classes.card}>
      <CardActionArea onClick={() => {}}>
        <CardContent sx={{ py: 3, px: 2 }} onClick={handleClick}>
          <Stack spacing={2} display="flex" alignItems="center">
            {icon}
            <Typography
              gutterBottom
              variant="subtitle2"
              component="div"
              sx={classes.cardLabel}
            >
              {label}
            </Typography>
            {children}
          </Stack>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

const AbTypeStep = ({ label, ...props }: AbTypeStep) => {
  const theme = useTheme();
  const classes = {
    title: {
      paddingTop: theme.spacing(15),
      paddingBottom: theme.spacing(5),
    },
    content: {
      display: "flex",
      justifyContent: "center",
      flexWrap: "wrap",
    },
  };

  return (
    <Box>
      <Typography sx={classes.title} variant="h1">
        1/3 Type of antibody
      </Typography>
      <Stack direction="row" spacing={1.5} sx={classes.content}>
        <TypeChoiceCard
          label="Commercial Antibody/Kit"
          icon={<CompanyIcon />}
          handleClick={() => props.handleChange("commercial")}
        >
          <Radio
            checked={props.selectedValue === "commercial"}
            onChange={(e) => props.handleChange(e.target.value)}
            value="commercial"
            size="small"
          />
        </TypeChoiceCard>
        <TypeChoiceCard
          label="Personal Antibody"
          icon={<UserWithBackgroundIcon />}
          handleClick={() => props.handleChange("personal")}
        >
          <Radio
            checked={props.selectedValue === "personal"}
            onChange={(e) => props.handleChange(e.target.value)}
            value="personal"
            size="small"
          />
        </TypeChoiceCard>
        <TypeChoiceCard
          label="Other/Custom Antibody"
          icon={<HorizontalThreeDotsIcon />}
          handleClick={() => props.handleChange("other")}
        >
          <Radio
            checked={props.selectedValue === "other"}
            onChange={(e) => props.handleChange(e.target.value)}
            value="other"
            size="small"
          />
        </TypeChoiceCard>
      </Stack>
      <Typography variant="subtitle2" sx={{ color: "grey.500", mt: 5 }}>
        Want to do a bulk upload? <Link href="/#">Contact us</Link>
      </Typography>
    </Box>
  );
};

export default AbTypeStep;
