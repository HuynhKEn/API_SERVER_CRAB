import React from "react";
import {
  Button,
  SafeAreaView,
  StatusBar,
  View,
  Text,
  TextInput,
  StyleSheet,
} from "react-native";
import Icon from "react-native-vector-icons/FontAwesome";
import { Context } from "../../context";
const Setting = () => {
  const { config, updateConfig } = React.useContext(Context);
  const [text, changeText] = React.useState(config.host);

  React.useEffect(() => console.log(host), [host]);
  function handleSetHost() {
    updateConfig({ ...config, host: text });
  }
  return (
    <View style={styles.container}>
      <TextInput
        style={{ height: 40, borderColor: "gray", borderWidth: 1 }}
        onChangeText={(text) => changeText(text)}
        value={text}
        placeholder="host"
      />
      <Button onPress={() => handleSetHost()} title="Cập nhật" />
    </View>
  );
};
export default Setting;
const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 100,
  },
});
