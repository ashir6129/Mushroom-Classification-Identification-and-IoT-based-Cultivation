import 'package:flutter/material.dart';
import 'screens/splash/splash_screen.dart';
import 'screens/home/home_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // No DB initialization needed now

  runApp(const PakMushroomsApp());
}

class PakMushroomsApp extends StatelessWidget {
  const PakMushroomsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Pak Mushrooms',
      theme: ThemeData(primarySwatch: Colors.green),
      home: const SplashScreen(),
      routes: {
        '/home': (_) => const HomeScreen(),
      },
    );
  }
}
