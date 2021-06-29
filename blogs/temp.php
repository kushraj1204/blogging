if (!function_exists("imageSizeOption")) {
    function imageSizeOption($image = '', $path = '', $class = 'img-fluid img-responsive', $src = true)
    {
        $empty = false;
        $returnImage = $image;
        if ($image == '' || !file_exists($path . $image)) {
            $empty = true;
            $path = '/img/';
            $returnImage = 'image-preview.png';
        }
        $returnImage = base_url($path . $returnImage);
        if ($src) {
            $imageArray['original'] = $empty ? $returnImage : base_url($path . $image);
            $imageArray['thumb'] = $empty ? $returnImage : base_url($path . 'thumb/' . $image);
            $imageArray['medium'] = $empty ? $returnImage : base_url($path . 'medium/' . $image);
            $imageArray['large'] = $empty ? $returnImage : base_url($path . 'large/' . $image);
            return $imageArray;
        }
        $imageArray['original'] = '<img src="' . $returnImage . '" class="' . $class . '">';
        $imageArray['thumb'] = '<img src="' . $returnImage . '" class="' . $class . '">';
        $imageArray['medium'] = '<img src="' . $returnImage . '" class="' . $class . '">';
        $imageArray['large'] = '<img src="' . $returnImage . '" class="' . $class . '">';
        return $imageArray;
        //return '<img src="' . $returnImage . '" class="' . $class . '">';
    }
}

if (!function_exists("imageDimension")) {
    function imageDimension($image = '', $path = '', $oldImage = '')
    {
        if ($image != '' && $path != '') {
            $imageDimensionModel = new \App\Models\ImagesDimensionModel();
            $imageDimension = $imageDimensionModel->first();
            $thumb_height = $imageDimension['thumb_height'];
            $thumb_width = $imageDimension['thumb_width'];
            $medium_height = $imageDimension['medium_height'];
            $medium_width = $imageDimension['medium_width'];
            $large_height = $imageDimension['large_height'];
            $large_width = $imageDimension['large_width'];

            $thumb_path = $path . '/thumb/';
            $medium_path = $path . '/medium/';
            $large_path = $path . '/large/';
            if (!is_dir($thumb_path)) {
                mkdir($thumb_path, 0777, TRUE);
            }
            if (!is_dir($medium_path)) {
                mkdir($medium_path, 0777, TRUE);
            }
            if (!is_dir($large_path)) {
                mkdir($large_path, 0777, TRUE);
            }

            if ($oldImage != '') {
                @unlink($thumb_path . $oldImage);
                @unlink($medium_path . $oldImage);
                @unlink($large_path . $oldImage);
            }

            /*$waterMark = 'Foodiplace.com';
            $waterMarkOptions = [
                'color'      => '#fff',
                'opacity'    => 0.1,
                //'withShadow' => true,
                'hAlign'     => 'center',
                'vAlign'     => 'center',
                'fontSize'   => 50
            ];*/
            $fullPath = $path . '/' . $image;
            $imageHandler = \Config\Services::image();
            $imageHandler->withFile($fullPath)
                //->text($waterMark, $waterMarkOptions)
                ->resize($thumb_height, $thumb_width, true, 'height')->save($thumb_path . $image);
            $imageHandler->withFile($fullPath)->resize($medium_height, $medium_width, true, 'height')->save($medium_path . $image);
            $imageHandler->withFile($fullPath)->resize($large_height, $large_width, true, 'height')->save($large_path . $image);
            return true;
        }
    }
}
