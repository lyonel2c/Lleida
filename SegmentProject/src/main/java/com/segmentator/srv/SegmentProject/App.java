package com.segmentator.srv.SegmentProject;

import larex.dataManagement.Page;
import larex.export.PageXMLWriter;

import java.io.File;

import org.opencv.core.Core;
import org.opencv.core.Size;
import larex.export.PageXMLReader;
import larex.export.PageXMLWriter;
import larex.export.SettingsReader;
import larex.export.SettingsWriter;
import larex.regionOperations.Merge;
import larex.regions.RegionManager;
import larex.segmentation.Segmenter;
import larex.segmentation.parameters.Parameters;
import larex.segmentation.result.ResultRegion;
import larex.segmentation.result.SegmentationResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;


/**
 * Hello world!
 *
 */
public class App 
{
    
	public static void listFilesForFolder(final File folder) {
        for (final File fileEntry : folder.listFiles()) {
            if (fileEntry.isDirectory()) {
                listFilesForFolder(fileEntry);
            } else {
                System.out.println(fileEntry.getName());
                createSegmentation(fileEntry.getName());
            }
        }
    }
    
	public static void createSegmentation(String nameFile) {
        
		//String str_path = "/home/lyonel/Dropbox/LLEIDA/BBVA/system/downloadPDF/";
		
		if(!(nameFile.contains(".directory")))
		{
		
			String str_path = "/home/lyonel/Dropbox/LLEIDA/BBVA/system/downloadPDF/";
			
			str_path += nameFile;
			System.out.println(str_path);
			//larex.dataManagement.Page conversion_pagina = new larex.dataManagement.Page("/home/lyonel/data/muestra.png");
			larex.dataManagement.Page conversion_pagina = new larex.dataManagement.Page(str_path);
	        conversion_pagina.initPage();
	        Size pagesize = conversion_pagina.getOriginal().size();
	        
	        Parameters parameters = new Parameters(new RegionManager(), (int) pagesize.height);
	        Segmenter segmenter = new Segmenter(parameters);
	        
	        SegmentationResult segmentationResult = segmenter.segment(conversion_pagina.getOriginal());
	        conversion_pagina.setSegmentationResult(segmentationResult);

	        System.out.println( "He segmentado mi primer png" );
	        
	        Document document = PageXMLWriter.getPageXML(segmentationResult, "temporal", (int) pagesize.width, (int) pagesize.height, "2018-03-19");
	        PageXMLWriter.saveDocument(document,nameFile,"/home/lyonel/Dropbox/LLEIDA/BBVA/system/downloadPDF/");

		}
		
		        
		

		
	}
	
	public static void main( String[] args )
    {
        System.out.println( "Initializing the process..." );
        String libreria_opencv = "/usr/local/share/OpenCV/java/libopencv_java2413.so";
        System.load(libreria_opencv);
        
        final File folder = new File("/home/lyonel/Dropbox/LLEIDA/BBVA/system/downloadPDF/");
        //This method walk through the directory described in the folder variable.
        listFilesForFolder(folder);
        
    }
    
    
    
    
    
}
