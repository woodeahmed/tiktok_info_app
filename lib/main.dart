import 'package:flutter/material.dart';
import 'package:flet/flet.dart';

void main() async {
  await flet.app(target: appMain);
}

Future<void> appMain(Page page) async {
  page.title = "TikTok Info App";
  await page.go("/"); // يوجه للـ main.py
}
