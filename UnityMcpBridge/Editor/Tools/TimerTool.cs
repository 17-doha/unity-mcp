using System;
using System.Collections;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;

namespace UnityMcpBridge.Editor.Tools
{
    /// <summary>
    /// Provides a timer tool for the Unity Editor.
    /// </summary>
    public static class TimerTool
    {
        public static object HandleCommand(JObject @params)
        {
            float timeValue = @params.Value<float?>("time") ?? 0f;
            string unit = @params.Value<string>("unit") ?? "sec";

            if (timeValue <= 0)
                return Helpers.Response.Error("Time value must be greater than zero.");

            TimerWindow.ShowWindow(timeValue, unit);
            return Helpers.Response.Success($"Timer started for {timeValue} {unit}.");
        }
    }

    public class TimerWindow : EditorWindow
    {
        private float remainingTime;
        private bool running;
        private string unit;

        public static void ShowWindow(float timeValue, string unit)
        {
            var window = GetWindow<TimerWindow>("Timer Tool");
            window.remainingTime = unit.ToLower() switch
            {
                "hrs" or "hours" => timeValue * 3600f,
                "min" or "minutes" => timeValue * 60f,
                _ => timeValue
            };
            window.unit = unit;
            window.running = true;
            window.Show();
        }

        private void OnGUI()
        {
            GUILayout.Label("Timer", EditorStyles.boldLabel);
            GUILayout.Label(FormatTime(remainingTime), EditorStyles.largeLabel);

            if (!running)
            {
                if (GUILayout.Button("Close")) Close();
            }
        }

        private void Update()
        {
            if (!running) return;
            if (remainingTime > 0)
            {
                remainingTime -= Time.deltaTime;
                Repaint();
            }
            else if (running)
            {
                running = false;
                ShowNotification(new GUIContent("Timer Finished!"));
            }
        }

        private string FormatTime(float time)
        {
            int hrs = Mathf.FloorToInt(time / 3600);
            int mins = Mathf.FloorToInt((time % 3600) / 60);
            int secs = Mathf.FloorToInt(time % 60);
            return $"{hrs:00}:{mins:00}:{secs:00}";
        }
    }
}