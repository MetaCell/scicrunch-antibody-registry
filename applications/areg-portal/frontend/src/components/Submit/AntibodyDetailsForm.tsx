import React from "react";
import { makeStyles } from '@mui/styles';
import { vars } from "../../theme/variables"
import { TextField, Paper, Grid, Typography, InputAdornment, IconButton } from "@mui/material";
import { AlertIcon } from "../icons";
import { useFormik } from "formik";
import * as yup from 'yup';
const { bannerHeadingColor, primaryTextColor } = vars;

const useStyles = makeStyles((theme?: any) => ({
    paper: {
        textAlign: "start",
        border: "1px solid #EAECF0",
        borderRadius: "1rem",
        boxShadow: " 0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03)",
        padding: "3rem",
        width: "720px"
    },
    formItem: {
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        "& .MuiInputBase-root.MuiOutlinedInput-root": {
            height: "2.5rem",
            boxShadow: "0px 1px 2px rgba(16, 24, 40, 0.05)",
            width: "300px"
        },
    },
    header: {
        color: bannerHeadingColor,
        paddingTop: 0
    },
    label: {
        color: bannerHeadingColor,
        marginBottom: "0.375rem"
    },
    lastInput: {
        width: "100%"
    }

}))


const validationSchema = yup.object().shape({
    catalogNumber: yup.string().required('The field is mandatory'),
});


const AntibodyDetailsForm = () => {
    const classes = useStyles();

    const formik = useFormik({
        enableReinitialize: true,
        initialValues: {
            email: '',
            catalogNumber: '',
            password: '',
        },
        validationSchema: validationSchema,
        onSubmit: (values) => {
            alert(JSON.stringify(values, null, 2));
        },
        validateOnChange: true
    });

    const {
        errors,
        touched,
        handleSubmit,
        isSubmitting,
        getFieldProps,
    } = formik;

    return (
        <Paper className={classes.paper}>
            <form onSubmit={handleSubmit}>
                <Grid
                    container
                    direction="column"
                    gap={3}
                    m={0}
                    width="100%"
                >
                    <Grid item>
                        <Typography variant="h1" className={classes.header}>3/3: Antibody Details</Typography>
                    </Grid>
                    <Grid item>
                        <Typography variant="h5" className={classes.label}>Catalog Number (Mandatory)</Typography>
                        <TextField
                            fullWidth
                            className="antibody-detail-catalogNumber"
                            name="catalogNumber"
                            value={formik.values.catalogNumber}
                            onChange={formik.handleChange}
                            {...getFieldProps("catalogNumber")}
                            error={Boolean(touched.catalogNumber && errors.catalogNumber)}
                            helperText={touched.catalogNumber && errors.catalogNumber}
                            InputProps={{
                                endAdornment: <InputAdornment position="end">{touched.catalogNumber && errors.catalogNumber && <AlertIcon />}</InputAdornment>
                            }}
                        />
                    </Grid>
                    <Grid item>
                        <Typography variant="h5" className={classes.label}>Vendor</Typography>
                        <TextField
                            fullWidth
                            className="antibody-detail-vendor"
                            name="vendor"
                            placeholder="Cell Signaling Technology"
                        />
                    </Grid>
                    <Grid item className={classes.formItem}>
                        <div>
                            <Typography variant="h5" className={classes.label}>Antibody Name</Typography>
                            <TextField
                                className="antibody-detail-name"
                                name="name"
                                placeholder="NeuN (D4G4O) XP® Rabbit mAb"
                            />
                        </div>
                        <div>
                            <Typography variant="h5" className={classes.label}>Host Species</Typography>
                            <TextField
                                className="antibody-detail-hostSpecies"
                                name="hostSpecies"
                                placeholder="Rabbit"
                            />
                        </div>
                    </Grid>
                    <Grid item className={classes.formItem}>
                        <div>
                            <Typography variant="h5" className={classes.label}>Target/Reactive Species</Typography>
                            <TextField
                                className="antibody-detail-targetORreactiveSpecies"
                                name="targetORreactiveSpecies"
                                placeholder="Human, Mouse, Rat"
                            />
                        </div>
                        <div>
                            <Typography variant="h5" className={classes.label}>Antibody Target</Typography>
                            <TextField
                                className="antibody-detail-target"
                                name="target"
                                placeholder="NeuN"
                            />
                        </div>
                    </Grid>
                    <Grid item className={classes.formItem}>
                        <div>
                            <Typography variant="h5" className={classes.label}>Clonality</Typography>
                            <TextField
                                className="antibody-detail-clonality"
                                name="clonality"
                                placeholder="Monoclonal"
                            />
                        </div>
                        <div>
                            <Typography variant="h5" className={classes.label}>Clone ID</Typography>
                            <TextField
                                className="antibody-detail-cloneID"
                                name="cloneID"
                                placeholder="Clone D4G4O"
                            />
                        </div>
                    </Grid>
                    <Grid item className={classes.formItem}>
                        <div>
                            <Typography variant="h5" className={classes.label}>Isotype</Typography>
                            <TextField
                                className="antibody-detail-isotype"
                                name="isotype"
                                placeholder="IgG"
                            />
                        </div>
                        <div>
                            <Typography variant="h5" className={classes.label}>Conjugate</Typography>
                            <TextField
                                className="antibody-detail-conjugate"
                                name="conjugate"
                                placeholder="Alexa Fluor 488"
                            />
                        </div>
                    </Grid>
                    <Grid item className={classes.formItem}>
                        <div>
                            <Typography variant="h5" className={classes.label}>Antibody Form/Format</Typography>
                            <TextField
                                className="antibody-detail-formORformat"
                                name="formORformat"
                                placeholder="Azide free"
                            />
                        </div>
                        <div>
                            <Typography variant="h5" className={classes.label}>Uniprot ID</Typography>
                            <TextField
                                className="antibody-detail-uniprotID"
                                name="uniprotID"
                                placeholder="A6NFN3"
                            />
                        </div>
                    </Grid>
                    <Grid item className={classes.formItem}>
                        <div>
                            <Typography variant="h5" className={classes.label}>Epitope</Typography>
                            <TextField
                                className="antibody-detail-epitope"
                                name="epitope"
                                placeholder="OTTHUMP00000018992"
                            />
                        </div>
                        <div>
                            <Typography variant="h5" className={classes.label}>Applications</Typography>
                            <TextField
                                className="antibody-detail-applications"
                                name="applications"
                                placeholder="ELISA, IHC, WB"
                            />
                        </div>
                    </Grid>
                    <Grid item>
                        <Typography variant="h5" className={classes.label}>Comments</Typography>
                        <TextField
                            className={classes.lastInput + " antibody-detail-comments"}
                            multiline
                            rows={5}
                            placeholder="Anything we should know about this antibody?"
                        />
                    </Grid>
                </Grid>
            </form>
        </Paper>
    )
}

export default AntibodyDetailsForm;