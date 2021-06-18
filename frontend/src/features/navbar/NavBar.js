import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Grid from '@material-ui/core/Grid';
import Link from 'next/link'
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import ButtonLink from '../../components/ButtonLink'
import { useSelector, useDispatch } from 'react-redux'
import {selectActiveTab, navbarSelected} from './navBarSlicer'



const useStyles = makeStyles((theme) => ({
  indicator: {
    backgroundColor: 'white',
  },
}));


function a11yProps(index) {
  return {
    id: `wrapped-tab-${index}`,
    'aria-controls': `wrapped-tabpanel-${index}`,
  };
}

export default function NavBar() {
  const classes = useStyles();
  // const [value, setValue] = React.useState(0);
  //
  const handleChange = (event, newValue) => {
    console.log('newValue', newValue)
    dispatch(navbarSelected(newValue))

  };

  const activeTab = useSelector(selectActiveTab)
  const dispatch = useDispatch()

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
          >
            <Link href="/" passHref>
              <Tab component="a" label="Gappers" />
            </Link>
            <Link href="/sentiment-analysis" passHref>
              <Tab component="a" disabled label="Sentiment Analysis" />
            </Link>
            <Link href="/trades" passHref>
              <Tab component="a" label="Trades" />
            </Link>
          </Tabs>
          </Grid>
          <Grid item>
            <Button component={ButtonLink} href={'/signin'} color="inherit">Login</Button>
            <Button component={ButtonLink} href={'/signup'} color="inherit">Sing me up!</Button>
            <Button component={ButtonLink} href={'/logout'} color="inherit">Log Out</Button>
          </Grid>
        </Grid>
        </Toolbar>
      </AppBar>
    </div>
  );
}
