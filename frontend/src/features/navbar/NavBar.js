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
import { selectActiveTab, navbarSelected } from './navBarSlicer'
import { selectUserIsLogedIn } from '../access/accessSlicer'
import MuiLink from "@material-ui/core/Link"

const CustomNextLink = ({href, alt}) => ({children, ...rest}) => (
<Link href={href} alt={alt}>
  <MuiLink {...rest}>
    {children}
  </MuiLink>
</Link>)

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
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
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

                <Tab to="/"  component={CustomNextLink({href: "/"})} label="Gappers" />
              {userIsLogedIn ?
                <Tab to="/trades"  component={CustomNextLink({href: "/trades"})} label="Trades" />
              : null }
            </Tabs>
          </Grid>
          <Grid item>
            {userIsLogedIn ?
                            <Link href="/logout" passHref><a>Log Out</a></Link>
                          : <Link href="/signin" passHref><a>Sign In</a></Link>
            }
          </Grid>
        </Grid>
        </Toolbar>
      </AppBar>
    </div>
  );
}
