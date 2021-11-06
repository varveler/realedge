import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Link from 'next/link'
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { useSelector, useDispatch } from 'react-redux'
import { selectActiveTab, navbarSelected } from './navBarSlicer'
import { selectUserIsLogedIn } from '../access/accessSlicer'

const useStyles = makeStyles((theme) => ({
  indicator: {
    backgroundColor: 'white',
  },
}));

// function a11yProps(index) {
//   return {
//     id: `wrapped-tab-${index}`,
//     'aria-controls': `wrapped-tabpanel-${index}`,
//   };
// }

export default function NavBar() {
  const classes = useStyles();
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const dispatch = useDispatch()
  const handleChange = (event, newValue) => {
    dispatch(navbarSelected(newValue))
  };

  const activeTab = useSelector(selectActiveTab)

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
        <Grid
          container
          direction="row"
          justify="space-around"
          alignItems="center"
        >
          <Grid item>
            <Typography >
              RealEdge
            </Typography>
          </Grid>
          <Grid item>
            <Tabs
              value={activeTab}
              indicatorColor="primary"
              onChange={handleChange}
              aria-label="site tabs navigation"
              classes={{
                indicator: classes.indicator
            }}>
              <Link href="/" as="/" passHref>
                <Tab component="a" label="Gappers" />
              </Link>
              {userIsLogedIn ?
                <Link href="/trades" as="/trades" passHref>
                  <Tab component="a" label="Trades" />
                </Link>
              : null }
            </Tabs>
          </Grid>
          <Grid item>
            {userIsLogedIn ?
                <Link href="/logout" as="/logout" passHref>
                  <Tab component="a" label="Log Out" />
                </Link>
              :
                <Link href="/signin" as="/signin" passHref>
                  <Tab component="a" label="Sign In" />
                </Link>
            }
          </Grid>
        </Grid>
        </Toolbar>
      </AppBar>
    </div>
  );
}
