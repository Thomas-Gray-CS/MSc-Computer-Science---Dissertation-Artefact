// UseState and UseEffect imported to handle states and effects.
// CSS from the relevant file is imported.
// Charts.js and the Bar chart module from this are installed, as are the applicable paramaters for this too.

import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import '../css/TeacherData.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';


// All of the applicable modules from ChartsJS are registed to be used in the chart.

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);


// TeacherData const is set using the current Teacher ID, with an empty
// array set called data.

const TeacherData = ({ teacherUserId }) => {
  const [data, setData] = useState([]);


  // data is fetched from the API, with thhe teacher Id being passed into the url

  useEffect(() => {
    const getProgressData = async () => {
      const res = await fetch(`/api/teacher/getProgressData/?teacher_id=${teacherUserId}`);
      const data = await res.json();
      setData(data);
    };
    

    // getProgressData is called with the current teacher user id being passed in the array.

    getProgressData();
  }, [teacherUserId]);


  // Constant for the chart data is made, with all applicable aspects of the chart passed in and
  // an array of the data defined. The structure for this is defined within the charts.js documents.

  const createChartData = (labels, dataPoints, color) => ({
    labels,
    datasets: [{
      label: 'Progress Score (%)',
      data: dataPoints.map(value => Math.round(value || 0)),
      backgroundColor: color,
    }]
  });


  // Chart is set as responsive and the scales are defined. This allows for better user navigation. The scale is
  // set from 0 to 100 as the p_known value is made a percentage in the backend.

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
    },
    scales: {
      y: { min: 0, max: 100 },
    },
  };


  // The charts are returned to the frontend, calling the applicable functions and data as provided.

  // Two charts are created, one for student data and one for the subtopics in the subject.
  // The raw numbers for the p_known scores are also taken and displayed for quick reading.

  return (
    <div className="teacherDataContainer">
      <h2 className="teacherDataHeading">Student Data</h2>
      {data.map((classObj) => {
        const subject = classObj.subject;
        if (!subject || !subject.students) return null;

        const studentData = createChartData(
          subject.students.map(student => student.student_name),
          subject.students.map(student => student.average_p_known),
          'rgba(54, 235, 63, 1)'
        );

        const subtopicData = createChartData(
          subject.subtopics.map(subtopic => subtopic.subtopic_name),
          subject.subtopics.map(subtopic => subtopic.mean_p_known),
          'rgba(83, 64, 255, 1)'
        );

          return (
            <div key={classObj.class_id} className="teacherDataChart">
              <h3 className="teacherDataChartSection">{classObj.class_name}</h3>
              <p className="teacherDataStudentScore">Class Average: {Math.round(subject.class_average_p_known || 0)}%</p>
              
              <div className="teacherDataChartMargin">
                <Bar data={studentData} options={chartOptions} />
              </div>
              {subject.subtopics && subject.subtopics.length > 0 && (
                <div className="teacherDataChartMargin">
                  <Bar data={subtopicData} options={chartOptions} />
                </div>
              )}
            </div>
          );
        })
      }
    </div>
  );
};


// The teacher data component is exported for use elsewhere.

export default TeacherData;
