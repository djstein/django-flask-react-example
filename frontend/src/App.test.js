import React from 'react';
import ReactDOM from 'react-dom';
import renderer from 'react-test-renderer';
import { shallow } from 'enzyme';

import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

import App from './App';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});

test('entire app snapshot', () => {
  const component = renderer.create(<App />);
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

test('App loads with correct intro text', () => {
  const rootApp = shallow(<App />);

  expect(rootApp.text()).toEqual(
    'Welcome to ReactTo get started, edit src/App.js and save to reload.'
  );

  expect(rootApp.contains(<div className="App-intro" />));
});
